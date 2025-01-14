import hashlib
import os
import yt_dlp
import time
from aiogram.types import FSInputFile
import subprocess
import math
import tempfile


def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()


def get_ffmpeg_path():
    """Укажите путь к FFmpeg, если он не в PATH."""
    return "ffmpeg"  # Убедитесь, что FFmpeg установлен и доступен


def split_file(file_path, max_size_mb=50):
    """
    Разбивает файл на части размером не более max_size_mb.
    Возвращает список путей к частям.
    """
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)

    if file_size_mb <= max_size_mb:
        return [file_path]  # Файл уже достаточно мал

    # Получаем длительность видео
    ffmpeg_path = get_ffmpeg_path()
    try:
        result = subprocess.run(
            [ffmpeg_path, "-i", file_path],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        output = result.stderr
        duration_line = [line for line in output.splitlines() if "Duration" in line][0]
        duration_str = duration_line.split("Duration:")[1].strip().split(",")[0]
        h, m, s = map(float, duration_str.split(":"))
        total_duration = int(h * 3600 + m * 60 + s)
    except Exception as e:
        raise RuntimeError(f"Не удалось получить длительность видео: {e}")

    # Рассчитываем длительность каждой части
    num_chunks = math.ceil(file_size_mb / max_size_mb)
    chunk_duration = math.ceil(total_duration / num_chunks)

    # Разбиваем видео на части
    base_name, ext = os.path.splitext(file_path)
    output_files = []
    start_time = 0

    for i in range(num_chunks):
        output_file = f"{base_name}_part{i + 1}{ext}"
        command = [
            ffmpeg_path,
            "-i",
            file_path,
            "-ss",
            str(start_time),
            "-t",
            str(chunk_duration),
            "-c",
            "copy",  # Используем stream copy, чтобы избежать повторной обработки
            output_file,
        ]
        subprocess.run(command, check=True)
        output_files.append(output_file)
        start_time += chunk_duration

    return output_files


async def download_and_send_media(bot, chat_id, url, media_type):
    # Используем временную директорию для сохранения файлов
    with tempfile.TemporaryDirectory() as temp_dir:


     
        
        ydl_opts = {
            'format': 'bestvideo[height<=480]+bestaudio/best' if media_type == 'video' else 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4' if media_type == 'video' else None,
         }

        try:
            start_time = time.time()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            end_time = time.time()
            elapsed_time = end_time - start_time

            # Проверяем размер файла и разбиваем его, если необходимо
            file_parts = split_file(filename, max_size_mb=50)

            # Отправляем все части поочередно
            for i, part in enumerate(file_parts, 1):
                media_file = FSInputFile(part)
                caption = f"Часть {i} из {len(file_parts)}.\n" if len(file_parts) > 1 else ""
                caption += f"Время загрузки: {elapsed_time:.2f} секунд."
                if media_type == "video":
                    await bot.send_video(chat_id, media_file, caption=caption)
                else:
                    await bot.send_audio(chat_id, media_file, caption=caption)

                os.remove(part)  # Удаляем отправленную часть

            os.remove(filename)  # Удаляем оригинальный файл

        except Exception as e:
            await bot.send_message(chat_id, f"Ошибка: {e}")
