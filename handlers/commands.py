from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

#импортируем тольео что созданную клавиатуру

import keyboards.inline_kb as in_kb

#импортируем функцию из function - которая url в человесеский вид приводит:
import handlers.function as hf

import url_storage as storage



router = Router()

@router.message(CommandStart())
async def cmd_download(message: Message):
    await message.reply("Скинь ссыль на ютуб чтобы скачать?")

@router.message(lambda message: "youtu.be" in message.text or "youtube.com" in message.text)
async def video_request(message: Message):
    url = message.text.strip()
    #url_id = hf.generate_url_id(url)
    url_id = hf.generate_url_id(url)
    storage.url_storage[url_id] = url
    storage.save_url_storage(storage.url_storage)
    storage.url_storage = storage.load_url_storage()
    #отправляем сообщение
    await message.answer("Выберите формат загрузки,", reply_markup= await in_kb.format_btn(url_id))




