import asyncio
import os
#1
#import telebot
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
    