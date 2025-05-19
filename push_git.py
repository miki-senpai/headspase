import os
import shutil
import subprocess

repo_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(repo_path)

json_dir = os.path.join(repo_path, 'json')

# Копируем все json-файлы из репо и подкаталогов в json/
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.json'):
            source_path = os.path.join(root, file)
            # Чтобы не копировать файлы из самой папки json (во избежание зацикливания)
            if os.path.commonpath([source_path, json_dir]) == json_dir:
                continue

            dest_path = os.path.join(json_dir, file)
            # Если нужно, можно добавлять уникальность в имена, если есть конфликты
            shutil.copy2(source_path, dest_path)
            print(f"Copied {source_path} -> {dest_path}")

# Коммитим (без ошибки, если нет изменений)
subprocess.run(["git", "commit", "-m", "Update all JSON files in json folder"], check=False)

# Сначала делаем pull, чтобы получить изменения с GitHub
subprocess.run(["git", "pull", "origin", "main"], check=True)

# Теперь пушим изменения
subprocess.run(["git", "push", "origin", "main"], check=True)

print("All JSON files pushed to GitHub in json/ folder (branch main)")