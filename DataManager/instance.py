from config import TOKEN, api_base_url, use_local_api
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot

if use_local_api:
    session = AiohttpSession(api=api_base_url)
    bot = Bot(TOKEN, session=session)
else:
    bot = Bot(TOKEN)





