from aiogram import F, Bot, Dispatcher, Router, types

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

from folder_manager import FolderManager
from DataManager.rename import Rename
from DataManager.get import Get
from DataManager.delate import Delete
from DataManager.move import MoveFile
from DataManager.Memory import MoveFileState, RenameState, CreateFolderState, DeleteState
import logging
from aiogram.types import Message
import os
import asyncio
from DataManager.db import UserInfo, Database
from DataManager import config
from DataManager import logger_config

class MyBot:
    def __init__(self, base_dir, bot):
        self.admin_id = config.admin_id
        self.base_dir = base_dir
        self.save_dir = r""
        self.bot = bot
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db = Database()
        self.folder_manager = FolderManager(base_path=os.path.dirname(os.path.abspath(__file__)), bot=self.bot, db=self.db)
        self.rename = Rename(self.bot, self.folder_manager)
        self.get = Get(self.bot, self.folder_manager)
        self.delete = Delete(self.bot, self.folder_manager)
        self.move = MoveFile(self.bot, self.folder_manager)    

        # Qui spostiamo i comandi dal main alla classe
        self.dp.message(CommandStart())(self.command_start_handler)
        self.dp.message(F.photo | F.document)(self.handle_message)
        self.dp.callback_query(F.data.startswith('prev_page:'))(self.process_callback_menage_page)
        self.dp.callback_query(F.data.startswith('next_page:'))(self.process_callback_menage_page)
        self.dp.callback_query(F.data.startswith('folder_entry:'))(self.handle_folder_callback)
        self.dp.callback_query(F.data == 'back')(self.handle_back_callback)
        self.dp.callback_query(F.data == "cancel")(self.handle_cancel_callback)
        self.dp.callback_query(F.data.startswith('file_action:'))(self.handle_action_file_callback)
        self.dp.callback_query(F.data.startswith('folder_action:'))(self.handle_action_folder_callback)
        self.dp.callback_query(F.data.startswith('rename:'))(self.rename.process_callback_rename)
        self.dp.message(RenameState.rename)(self.rename.rename_entry)
        self.dp.callback_query(F.data.startswith('get:'))(self.get.process_callback_get)
        self.dp.callback_query(F.data.startswith('delete:'))(self.delete.process_callback_delete)
        self.dp.callback_query(F.data.startswith('move:'))(self.move.show_destination_folders)
        self.dp.callback_query(F.data.startswith('enter_folder:'))(self.handle_enter_folder_callback)
        self.dp.callback_query(F.data.startswith('move_to_folder:'))(self.handle_move_to_folder_callback)
        self.dp.message(F.text)(self.filter_entries)
        self.dp.message(Command("create_folder"))(self.handle_create_folder)
        self.dp.message(CreateFolderState.name)(self.handle_folder_name)
        
    async def command_start_handler(self, message: Message) -> None:
        user_id = UserInfo(message).user_id
        try:
            if user_id == self.admin_id:
                keyboard = self.folder_manager.list_entries(None, 0)
                await message.answer("Select element:", reply_markup=keyboard)
        except Exception as ex:
            logging.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{user_id}:{ex}")  

    async def handle_message(self, message: types.Message):
        user_id = UserInfo(message).user_id
        try:
            if user_id == self.admin_id:
                    file_path, file_name = await self.folder_manager.ReciveImage(message)
                    await message.answer(f"File saved in {file_path}")
                    self.folder_manager.save_file(file_path, self.save_dir)
        except Exception as ex:
            logging.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  
        return      
            
    async def process_callback_menage_page(self, callback_query: types.CallbackQuery):
        try:
            page = int(callback_query.data.split(':')[1])
            keyboard = self.folder_manager.list_entries(None, page)
            await self.bot.edit_message_text("Select element:", callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard)
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  
            
    async def handle_folder_callback(self, callback_query: types.CallbackQuery):
        try:       
            folder_id = int(callback_query.data.split(':')[1])
            folder_name = self.db.get_entry(folder_id)
            self.folder_manager.change_folder(folder_name)
            keyboard = self.folder_manager.list_entries(None, 0)
            await callback_query.message.edit_text("Select element:", reply_markup=keyboard)
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  
            
    async def handle_back_callback(self, callback_query: types.CallbackQuery):
        try:    
            self.folder_manager.go_back()
            keyboard = self.folder_manager.list_entries(None, 0)
            await callback_query.message.edit_text("Select element:", reply_markup=keyboard)
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  
            
    async def handle_cancel_callback(self, callback_query: types.CallbackQuery):
        try:
            user_id = callback_query.from_user.id
            await callback_query.message.edit_text("Operation delated")
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  
        
    async def handle_action_file_callback(self, callback_query: types.CallbackQuery, state: FSMContext):
        try:
            file_id = int(callback_query.data.split(':')[1])
            file_name = self.db.get_entry(file_id)
            await state.set_state(MoveFileState.file_name)    
        
            await state.update_data(file_name=file_name) # Puoi anche salvare dei dati nello stato
            keyboard = self.folder_manager.file_actions(file_id)
            await callback_query.message.edit_text(f"Action for file {file_name}:", reply_markup=keyboard)
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  
        
    async def handle_action_folder_callback(self, callback_query: types.CallbackQuery, state: FSMContext):
        try:
            folder_id = int(callback_query.data.split(':')[1])
            folder_name = self.db.get_entry(folder_id)
            await state.set_state(MoveFileState.file_name)
            await state.update_data(folder_name=folder_name)
            keyboard = self.folder_manager.folder_actions(folder_id)
            await callback_query.message.edit_text(f"Action for folder {folder_name}:", reply_markup=keyboard)
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")         
        
    async def handle_enter_folder_callback(self, callback_query: types.CallbackQuery):
        try:
            folder_id = int(callback_query.data.split(':')[1])
            folder_name = self.db.get_entry(folder_id)
            if self.folder_manager.change_folder(folder_name):
                await self.move.show_destination_folders(callback_query)
            else:
                await callback_query.message.edit_text("cannot open directory")
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  
        
    async def handle_move_to_folder_callback(self, callback_query: types.CallbackQuery, state: FSMContext):
        try:
            folder_id = int(callback_query.data.split(':')[1])
            folder_path = self.folder_manager.get_entry(folder_id)
            await self.move.handle_move_to_folder_callback(callback_query, folder_path, state)
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}") 
            
    async def filter_entries(self, message: types.Message):
        try:
            filter_text = message.text
            user_id = message.from_user.id
            if user_id == self.admin_id:
                keyboard = self.folder_manager.list_entries(filter_text, 0)
                await message.answer("Select element:", reply_markup=keyboard)
        except Exception as ex:
            logger_config.logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")  

    async def handle_create_folder(message: types.Message, state: FSMContext):
        await CreateFolderState.name.set()
        await message.answer("Please enter the name of the folder you want to create:")

    async def handle_folder_name(message: types.Message, state: FSMContext):
        save_dir = ""
        folder_name = os.path.join(save_dir, message.text)
        try:
            os.mkdir(folder_name)
            await message.answer(f"Folder {folder_name} created succesfully!")
        except Exception as ex:
            await message.answer(f"{ex}")
        finally:        
            await state.clear()        
    
