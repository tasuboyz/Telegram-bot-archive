from aiogram import types
import os
import shutil
from aiogram.fsm.context import FSMContext
from .db import Database

class Delete:
    def __init__(self, bot, folder_manager):
        self.bot = bot
        self.folder_manager = folder_manager
        self.db = Database()

    async def process_callback_delete(self, callback_query: types.CallbackQuery, state: FSMContext):
        try:
            file_id = int(callback_query.data.split(':')[1])
            file_name = self.db.get_entry(file_id)
            file_path = os.path.join(self.folder_manager.current_path, file_name)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            self.db.delete_entry(file_id)
            await callback_query.answer(f"{file_name} eliminato con successo!")
        finally:
            await state.clear()





