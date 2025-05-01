from telethon.sync import TelegramClient
import json
import os
import sys

# Получаем переменные окружения
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_id = os.getenv("CHANNEL_ID")

# Проверяем наличие всех необходимых переменных
if not all([api_id, api_hash, channel_id]):
    print("Ошибка: Не все необходимые переменные окружения установлены")
    print("Требуются: API_ID, API_HASH, CHANNEL_ID")
    sys.exit(1)

try:
    api_id = int(api_id)
    channel_id = int(channel_id)
except ValueError:
    print("Ошибка: API_ID и CHANNEL_ID должны быть числами")
    sys.exit(1)

output_file = "tracks.json"

try:
    with TelegramClient("session", api_id, api_hash) as client:
        # Получаем сообщения из канала по его ID
        messages = client.get_messages(channel_id, limit=50)

        tracks = []
        for msg in messages:
            if msg.audio:
                track_info = {
                    "title": msg.audio.title or "Без названия",
                    "performer": msg.audio.performer or "Неизвестен",
                    "duration": msg.audio.duration,
                    "file_name": msg.file.name or "",
                    "message_id": msg.id
                }
                tracks.append(track_info)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(tracks[::-1], f, ensure_ascii=False, indent=2)

        print(f"Сохранено {len(tracks)} треков в {output_file}")

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")
    sys.exit(1)
