from aiogram import Dispatcher, Bot

from config import TOKEN

from db import Database

bot = Bot(token=TOKEN)
dp = Dispatcher()

db = Database()

async def launch():
    await dp.start_polling(bot)