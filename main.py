import os

from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

import logging
import asyncio
import sys

from DataManager import instance
from bot import MyBot

async def main() -> None:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        my_bot = MyBot(base_dir, instance.bot)
        await my_bot.dp.start_polling(my_bot.bot)
    except Exception as ex:
        logging.error(f"Errore durante l'esecuzione di command_start_handler: {ex}", exc_info=True)
    
if __name__ == '__main__':       
    asyncio.run(main())
