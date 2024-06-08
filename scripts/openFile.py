import subprocess
import sys

# Получение параметров командной строки
params = sys.argv[1:]  # Первым элементом в sys.argv является имя скрипта
file_path = params[0]


# Открываем файл с помощью программы по умолчанию
try:
    subprocess.run(['start', file_path], shell=True, check=True)
    print(f"{file_path} успешно открыт.")
except Exception as e:
    print(f"Ошибка при открытии {file_path}: {e}")
