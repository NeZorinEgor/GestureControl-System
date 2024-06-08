import os
import shutil
import subprocess

save_dir = "../../../scripts"


def startScript(path, string="", force=100):
    # Параметры, которые нужно передать
    params = [str(string), str(force)]

    # Запуск файла с параметрами
    result = subprocess.run(['python', path] + params, capture_output=True, text=True)
    return result.stdout, result.stderr


def saveScript(path, name=None, save_dir=None):

    if save_dir is None:
        save_dir = ''

    if name is None:
        name = os.path.basename(path)

    # Полный путь к новому файлу
    new_file_path = os.path.join(save_dir, name)

    # Создаем новую папку, если она не существует
    os.makedirs(save_dir, exist_ok=True)

    # Перемещаем и переименовываем файл
    shutil.copy2(path, new_file_path)

    return new_file_path


def deleteScript(path):
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        return False
