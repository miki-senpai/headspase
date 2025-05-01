from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Используйте ваши API_ID и API_HASH
api_id = '26114022'
api_hash = 'ed6bc106635c0cc986d99e980d051242'

# Создаем клиент
client = TelegramClient(StringSession(), api_id, api_hash)
client.start()

# Получаем строку сессии
session_string = client.session.save()
print(f"SESSION_STRING: {session_string}")

client.disconnect()
