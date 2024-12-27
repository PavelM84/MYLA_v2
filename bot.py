import asyncio
import os
#1
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Хэндлер для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Напишите команду 'Login', чтобы открыть YouTube.")

# Хэндлер для команды 'Login'
@dp.message_handler(lambda message: message.text.lower() == 'login')
async def open_youtube(message: types.Message):
    youtube_url = "https://www.youtube.com"  # Ссылка на YouTube
    await message.reply(f"Открываю YouTube для вас: {youtube_url}")

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)


#/1

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import callaback, commands

#2

#@bot.message_handler(commands=['info'])
#def send_show(message):
#    bot.reply_to(message, "Вот, что я умею:")

#2/



async def main():
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token)
    dp = Dispatcher()
    try:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        dp.include_router(commands.router)
        dp.include_router(callaback.router)
        print('Bot started')
        await dp.start_polling(bot)
        await bot.session.close()
    except Exception as ex:
        print(f"There is exeption: {ex}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    
