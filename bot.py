import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from dotenv import load_dotenv

from handlers import callaback, commands

# Настройка логирования
logging.basicConfig(
    filename="bot_requests.log",  # Файл для логов
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат записи
)

def log_request(user_id, message):
    logging.info(f"User ID: {user_id}, Message: {message}")

async def start_bot():
    """Функция для запуска бота с обработкой сетевых ошибок."""
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logging.error("Ошибка: BOT_TOKEN не найден в .env файле!")
        return

    bot = Bot(token)
    dp = Dispatcher()

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    dp.include_router(commands.router)
    dp.include_router(callaback.router)

    while True:
        try:
            logging.info("Бот запущен и ожидает сообщения...")
            await dp.start_polling(bot)
        except TelegramNetworkError as e:
            logging.error(f"Ошибка сети: {e}. Переподключение через 5 секунд...")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Критическая ошибка: {e}")
            break  # Прерываем выполнение при фатальной ошибке
        finally:
            await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print('Exit')
