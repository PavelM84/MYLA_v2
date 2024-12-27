import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Токен бота, извлекаемый из .env
API_TOKEN = os.getenv('BOT_TOKEN')

# Создаем экземпляры бота и диспетчера
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

# Функция для запуска бота
async def main():
    try:
        print('Bot started')
        # Запуск бота
        await dp.start_polling()
    except Exception as ex:
        print(f"There is an exception: {ex}")

if __name__ == '__main__':
    try:
        # Запуск асинхронной функции
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
