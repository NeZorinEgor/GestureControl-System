from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import sys

# Получение параметров командной строки
params = sys.argv[1:]  # Первым элементом в sys.argv является имя скрипта
state = int(params[-1])

# Получение всех аудио-устройствs
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Получение текущего состояния выключения звука (True - звук выключен, False - звук включен)
#is_muted = volume.GetMute()
#print(f"Звук выключен: {is_muted}")

# Отключение/включение звука
volume.SetMute(state, None)  # 1 - выключить звук, 0 - включить звук
