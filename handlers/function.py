import hashlib
import os
import yt_dlp
import time
from aiogram.types import FSInputFile



def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()


async def download_and_send_media(bot, chat_id, url, media_type):
     
    ydl_opts = {
        'format': 'best[height<=480]' if media_type == 'video' else 'bestaudio/best',
       'outtmpl': f"downloads/%(title)s.{'mp4' if media_type == 'video' else 'm4a'}",
    } 

#    ydl_opts = {
#        'format': 'best[exp=mp4]' if media_type == 'video' else 'bestaudio[exp=m4a]/best',
#        'outtmpl': f'downloads/%(title)s.{'mp4' if media_type == 'video' else 'm4a'}',

# попытка номер 2  --          потом разберксь
#ydl_opts = {
#   'format': 'best',  # Автоматический выбор лучшего доступного формата
#        'format': 'best[exp=mp4]' if media_type == 'video' else 'bestaudio[exp=m4a]/best',
#       'outtmpl': f'downloads/%(title)s.{'mp4' if media_type == 'video' else 'm4a'}',
#    }
  
    try:
        start_time = time.time()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        end_time = time.time()
        elapsed_time = end_time - start_time

        media_file = FSInputFile(filename)
        if media_type == "video":
            await bot.send_video(chat_id, media_file, caption=f"Вот видео. Время загрузки {elapsed_time:.2f} секунд.")
        else:
            await bot.send_audio(chat_id, media_file, caption=f"Вот аудио. Время загрузки {elapsed_time:.2f} секунд.")

        os.remove(filename)

    except Exception as e:
        await bot.send_message(chat_id, f"Ошибка: {e}")
