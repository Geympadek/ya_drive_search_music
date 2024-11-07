from loader import *

from aiogram import types
from aiogram.types import Message, CallbackQuery, MessageEntity
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import utils
import search
import menu
import config

import asyncio

from collections import defaultdict

@dp.message(Command("start"))
async def on_start(msg: Message, state: FSMContext):
    await state.set_state("menu")

    text = "Этот бот ищет песни на яндекс диске."
    await bot.send_message(msg.chat.id, text= text)

    await on_search(msg, state)

async def show_search(msg: Message):
    text = "Искать песню по названию"
    await bot.send_message(chat_id=msg.chat.id, text=text, reply_markup=menu.search_kb)

async def show_settings(msg: Message):
    LINK = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={config.YA_CLIENT_ID}"
    text=\
    "Для работы бота нужен <i>токен Яндекс диска</i>.\n"\
    f"Перейдите по <a href=\"{LINK}\">ссылке</a> и скопируйте токен. Он будет выглядеть вот так:\n"\
    "<code>y0_AgBBCCBFjjs7AAy6sgABBAXeDOR6AASCru-e74tGvKgpgQQ-E5vIezFEWc</code>"

    await bot.send_message(msg.chat.id, text=text, parse_mode="html")

@dp.callback_query()
async def on_query(query: CallbackQuery, state: FSMContext):
    if query.data == "search":
        await state.set_state("search")
        await bot.send_message(query.message.chat.id, text="Введите название песни")
    if query.data.startswith("song:"):
        await state.set_state("menu")
        
        user_data = await state.get_data()
        id = int(query.data.split(':', 1)[1])

        song_data = user_data.get("song_data", {})[id]

        path = song_data["path"]
        url = search.gen_url(db.get(query.from_user.id)["ya_token"], path)
        
        audio_task = bot.send_audio(query.message.chat.id, audio=types.URLInputFile(url), title=song_data["name"], performer="🍊🍊🍊")
        
        load_msg = await bot.send_message(query.message.chat.id, text="🍊 Загружаем песню...")

        await audio_task

        await bot.delete_message(query.message.chat.id, load_msg.message_id)

async def update_token(msg: Message, state: FSMContext):
    await show_settings(msg)
    await state.set_state("settings")

@dp.message(Command("search"))
async def on_search(msg: Message, state: FSMContext):
    token = db.get(msg.from_user.id).get("ya_token") 
    if token is None or not search.check_token(token):
        update_token(msg, state)
        return

    await state.set_state("menu")
    await show_search(msg)

@dp.message(StateFilter("settings"))
async def on_token_set(msg: Message, state: FSMContext):
    token = msg.text

    text = ""

    if not search.check_token(token):
        text = "Не удалось подключиться к яндексу. Перепроверьте токен и попробуйте еще раз."
    else:
        text = "Токен успешно установлен."

        db.get(msg.from_user.id)["ya_token"] = token
        db.save()
    
    await bot.send_message(msg.chat.id, text=text)

@dp.message(StateFilter("search"))
async def on_music_search(msg: Message, state: FSMContext):
    query = msg.text

    best = search.get_best(db.get(msg.from_user.id)["ya_token"], query, 5)

    song_data = {}

    kb = []

    for i, el in enumerate(best):
            kb.append([menu.get_song_btn(el["name"].split(".")[0], i)])  # Use song_id as callback_data
            song_data[i] = el

    await state.update_data(song_data = song_data)

    kb = types.InlineKeyboardMarkup(inline_keyboard=kb)
    
    if len(best) == 0:
        await bot.send_message(msg.chat.id, "По запросу ничего не найдено.")
    else:
        await bot.send_message(msg.chat.id, f"По запросу `{query}` нашлось следующее: ", reply_markup=kb)


if __name__ == "__main__":
    asyncio.run(launch())

    # print(utils.similarity(query, song))
    # search.get_token()