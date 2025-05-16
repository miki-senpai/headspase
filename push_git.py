import os
import shutil
import subprocess

# Путь к папке с JSON-файлами
source_root = r'G:\Мой диск\Headspase'

# Путь к Git-репозиторию — текущая директория скрипта
repo_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(repo_path)

# Рекурсивно ищем все .json файлы и копируем их в репозиторий
for dirpath, dirnames, filenames in os.walk(source_root):
    for file in filenames:
        if file.endswith('.json'):
            source_file = os.path.join(dirpath, file)
            # Получаем относительный путь внутри Headspase
            relative_path = os.path.relpath(source_file, source_root)
            destination_file = os.path.join(repo_path, relative_path)

            # Создаём папки в репозитории, если нужно
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)

            # Копируем файл
            shutil.copy2(source_file, destination_file)
            print(f'Copied: {relative_path}')

# Добавляем, коммитим и пушим все изменения
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Update all JSON files"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("✅ All JSON files uploaded to GitHub (branch main)")
