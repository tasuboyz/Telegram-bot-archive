from ast import Dict
from aiogram import types
import os
import shutil
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class MoveFile:
    def __init__(self, bot, folder_manager):
        self.bot = bot
        self.folder_manager = folder_manager

    async def show_destination_folders(self, callback_query):
        folders_keyboard = self.folder_manager.list_folders()
        if not folders_keyboard.inline_keyboard:
            await callback_query.message.edit_text("Nessuna cartella disponibile")
        else:
            await callback_query.message.edit_text("Seleziona una cartella di destinazione:", reply_markup=folders_keyboard)

    async def handle_move_to_folder_callback(self, callback_query: types.CallbackQuery, destination_path, state):
        folder_name = os.path.basename(destination_path)
        Dict = await state.get_data()
        file_path = Dict['file_name']
        try:
            if file_path:
                file_name = os.path.basename(file_path)
                src_path = os.path.join(self.folder_manager.current_path, file_name)
                dest_file_path = f"{destination_path}//{file_name}"
 
                if os.path.exists(dest_file_path):
                    os.remove(dest_file_path)

                shutil.move(src_path, dest_file_path)
                await callback_query.message.edit_text(f"File {file_name} spostato nella cartella {folder_name}")
            elif folder_name:
                src_path = os.path.join(self.folder_manager.current_path, folder_name)
                shutil.move(src_path, destination_path)
                await callback_query.message.edit_text(f"Cartella {folder_name} spostata nella cartella {folder_name}")
        finally:
            await state.clear()


