import json
import os

#
import subprocess
#

URL_STORAGE_FILE = "url_storage_json"

#
COOKIES_FILE = "cookies.txt"
#

def load_url_storage():
    if os.path.exists(URL_STORAGE_FILE):
        with open(URL_STORAGE_FILE, "r") as file:
            return json.load(file)
    return{}

def save_url_storage(data):
    with open(URL_STORAGE_FILE, "w") as file:
        json.dump(data, file)


#
def download_video(url):
    # Команда для yt-dlp с использованием cookies
    command = [
        "yt-dlp",
        "--cookies", COOKIES_FILE,  # Передача файла cookies
        url
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при загрузке видео: {e}")



url_storage = load_url_storage()
