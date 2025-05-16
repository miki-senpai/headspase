import os
import json
import asyncio
from telegram import Bot
from telegram.constants import ChatAction
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

# === SETTINGS ===
BOT_TOKEN = '7717263989:AAFqv-4ob5-c6o1eFd2-6zFNvSRH5rbta3s'
CHANNEL_ID = '@headspase_music'
MAIN_FOLDER = r'G:\Мой диск\Headspase\Main'


MUSIC_FOLDER = r'G:\Мой диск\Headspase\АРТИСТ\АЛЬБОМ'
ARTIST_FOLDER = r'G:\Мой диск\Headspase\АРТИСТ'

bot = Bot(token=BOT_TOKEN)

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def upload_music():
    all_files = os.listdir(MUSIC_FOLDER)
    mp3_files = [f for f in all_files if f.lower().endswith('.mp3')]
    cover_file_id = None

    # === Upload album cover ===
    for file in all_files:
        if file.lower().endswith('.jpg'):
            cover_path = os.path.join(MUSIC_FOLDER, file)
            print(f'[COVER] Uploading album cover: {file}')
            try:
                with open(cover_path, 'rb') as cover_file:
                    sent_msg = await bot.send_photo(chat_id=CHANNEL_ID, photo=cover_file)
                    cover_file_id = sent_msg.photo[-1].file_id
                print(f'[COVER OK] file_id: {cover_file_id}\n')
                os.remove(cover_path)
            except Exception as e:
                print(f'[COVER ERROR] {file}: {e}\n')
            break

    if not mp3_files:
        print('\n[INFO] No MP3 files found.')
        return

    total = len(mp3_files)
    albums_json_path = os.path.join(MAIN_FOLDER, 'albums.json')
    artists_json_path = os.path.join(MAIN_FOLDER, 'artists.json')
    albums_data = load_json(albums_json_path)
    artists_data = load_json(artists_json_path)

    for idx, filename in enumerate(mp3_files, start=1):
        file_path = os.path.join(MUSIC_FOLDER, filename)

        try:
            audio = MP3(file_path, ID3=EasyID3)
            title = audio.get('title', [os.path.splitext(filename)[0]])[0]
            performer = audio.get('artist', ['Unknown Artist'])[0]
            album = audio.get('album', ['Unknown Album'])[0]
            genre = audio.get('genre', ['Unknown Genre'])[0]

            await bot.send_chat_action(chat_id=CHANNEL_ID, action=ChatAction.TYPING)

            with open(file_path, 'rb') as audio_file:
                sent_msg = await bot.send_audio(
                    chat_id=CHANNEL_ID,
                    audio=audio_file,
                    title=title,
                    performer=performer
                )

            file_id = sent_msg.audio.file_id
            print(f'\n[OK] {filename} | file_id: {file_id}')

            # === Save to artist-specific JSON ===
            performer_safe = sanitize_filename(performer)
            performer_file = os.path.join(MUSIC_FOLDER, f"{performer_safe}.json")

            artist_tracks = load_json(performer_file)
            artist_tracks.append({
                'album': album,
                'title': title,
                'performer': performer,
                'genre': genre,
                'file_id': file_id,
                'cover_file_id': cover_file_id
            })
            save_json(performer_file, artist_tracks)

            os.remove(file_path)

            # === Update albums.json ===
            if not any(a for a in albums_data if a['album'] == album and a['performer'] == performer):
                albums_data.append({
                    'album': album,
                    'performer': performer,
                    'cover_file_id': cover_file_id
                })
                save_json(albums_json_path, albums_data)
                print(f'[ALBUM ADDED] {album} — {performer}')

            # === Update artists.json and upload artist photo if new ===
            if not any(a for a in artists_data if a['name'] == performer):
                # Найти фото артиста
                # Найти любой .jpg файл в папке ARTIST_FOLDER
                artist_image = next(
                    (os.path.join(ARTIST_FOLDER, f) for f in os.listdir(ARTIST_FOLDER) if f.lower().endswith('.jpg')),
                    None
                )


                if artist_image:
                    try:
                        with open(artist_image, 'rb') as img:
                            sent_photo = await bot.send_photo(chat_id=CHANNEL_ID, photo=img)
                            artist_file_id = sent_photo.photo[-1].file_id
                        os.remove(artist_image)
                        print(f'[ARTIST IMAGE OK] {performer}: {artist_file_id}')
                        artists_data.append({
                            'name': performer,
                            'file_id': artist_file_id
                        })
                        save_json(artists_json_path, artists_data)
                    except Exception as e:
                        print(f'[ARTIST IMAGE ERROR] {performer}: {e}')
                else:
                    print(f'[ARTIST IMAGE NOT FOUND] {performer}')

        except Exception as e:
            print(f'\n[ERROR] {filename}: {e}')

    print(f'\n\n[UPLOAD END]')

if __name__ == "__main__":
    asyncio.run(upload_music())
