from http import server
import os
from datetime import datetime
from aiogram import F, Bot, Dispatcher, Router, types

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

from aiogram.types import Message
from aiogram.utils.markdown import hbold
import logging
import asyncio
import sys

from DataManager import config
from DataManager import logger_config
from bot import MyBot

# dp.middleware.setup(LoggingMiddleware())

# @dp.message_handler(Command("create_folder"))
# async def handle_create_folder(message: types.Message, state: FSMContext):
#     await CreateFolderState.name.set()
#     await message.answer("Per favore, inserisci il nome della cartella che vuoi creare:")

# @dp.message(CreateFolderState.name)
# async def handle_folder_name(message: types.Message, state: FSMContext):
#     folder_name = os.path.join(save_dir, message.text)
#     try:
#         os.mkdir(folder_name)
#         await message.answer(f"Cartella {folder_name} creata con successo!")
#     except Exception as ex:
#         await message.answer(f"Errore durante la creazione della cartella: {ex}")
#     finally:        
#         await state.clear()        

async def main() -> None:
    try:
        bot_token = config.bot_token
        admin_id = config.admin_id
        if config.use_local_api:
            session = AiohttpSession(
                api=TelegramAPIServer.from_base(config.api_base_url)
            )
            bot = Bot(bot_token, session=session)
        else:
            bot = Bot(bot_token)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)
        my_bot = MyBot(base_dir, bot)
        await my_bot.dp.start_polling(my_bot.bot)
    except Exception as ex:
        logging.error(f"Errore durante l'esecuzione di command_start_handler: {ex}", exc_info=True)
    
if __name__ == '__main__':       
    asyncio.run(main())
