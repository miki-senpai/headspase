from telethon.sync import TelegramClient
import json
import os

api_id = int(os.getenv("26114022"))
api_hash = os.getenv("ed6bc106635c0cc986d99e980d051242")
channel_id = int(os.getenv("1002599688450"))  # ID канала

output_file = "tracks.json"

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

    print(f"Saved {len(tracks)} tracks to {output_file}")
