from aiogram import types
import os
import shutil
from .db import Database

class Get:
    def __init__(self, bot, folder_manager):
        self.bot = bot
        self.folder_manager = folder_manager
        self.db = Database()

    async def process_callback_get(self, callback_query: types.CallbackQuery):
        file_id = int(callback_query.data.split(':')[1])
        file_name = self.db.get_entry(file_id)
        file_path = os.path.join(self.folder_manager.current_path, file_name)
        if os.path.isdir(file_path):
            zip_path = shutil.make_archive(file_path, 'zip', file_path)
            input_file = types.FSInputFile(file_path)
            await self.bot.send_document(callback_query.from_user.id, input_file)
            os.remove(zip_path)
        else:
            input_file = types.FSInputFile(file_path)
            await self.bot.send_document(callback_query.from_user.id, input_file)



