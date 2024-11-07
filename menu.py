from aiogram import types
from loader import *

search_btn = types.InlineKeyboardButton(text="Поиск 🔎", callback_data="search")
search_kb = types.InlineKeyboardMarkup(inline_keyboard=[[search_btn]])

def get_song_btn(song: str, id: int):
    return types.InlineKeyboardButton(text=f"🍊 {song}", callback_data=f"song:{id}")