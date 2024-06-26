from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import sys

# Получение параметров командной строки
params = sys.argv[1:]  # Первым элементом в sys.argv является имя скрипта
force = float(params[-1])

# Получение всех аудио-устройств
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Получение текущего уровня громкости
current_volume = volume.GetMasterVolumeLevelScalar()
#print(f"Текущий уровень громкости: {current_volume * 100}%")

# Установка громкости (значение от 0.0 до 1.0)
volume.SetMasterVolumeLevelScalar(force, None)  # 50% громкости

# Установка громкости в децибелах
# volume.SetMasterVolumeLevel(-20.0, None)


