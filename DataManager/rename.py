from aiogram import types
from aiogram.filters import Filter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F, Bot, Dispatcher, Router, types
import os
from .Memory import RenameState

class Rename:
    def __init__(self, bot, folder_manager):
        self.bot = bot
        self.folder_manager = folder_manager
        
    async def rename_entry(self, message: types.Message, state: FSMContext):
        new_name = message.text
        Dict = await state.get_data()
        entry_id = Dict['entry_id']
        old_path = self.folder_manager.get_entry(entry_id)
        percorso = os.path.dirname(os.path.abspath(old_path))
        new_name_path = f"{percorso}//{new_name}"
        os.rename(old_path, new_name_path)
        self.folder_manager.update_entry(entry_id, new_name_path)
        await message.answer(f"Rinomina avvenuta con successo. Nuovo nome: {new_name}")
    
    async def process_callback_rename(self, callback_query: types.CallbackQuery, state):
        try:
            entry_id = int(callback_query.data.split(':')[1])
            entry_name = self.folder_manager.get_entry(entry_id)
            file_name = os.path.basename(entry_name)
            sent_message = await self.bot.send_message(callback_query.from_user.id, f"Inserisci il nuovo nome per {file_name}:")
            await state.set_state(RenameState.rename)
            await state.update_data(entry_id=entry_id)
            await self.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)            
        except Exception as e:
            await self.bot.send_message(callback_query.from_user.id, f"Errore durante la rinomina: {e}")






