from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Получение всех аудио-устройств
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Получение текущего уровня громкости
current_volume = volume.GetMasterVolumeLevelScalar()
print(f"Текущий уровень громкости: {current_volume * 100}%")

# Установка громкости (значение от 0.0 до 1.0)
volume.SetMasterVolumeLevelScalar(1., None)  # 50% громкости

# Установка громкости в децибелах
# volume.SetMasterVolumeLevel(-20.0, None)

# Получение текущего состояния выключения звука (True - звук выключен, False - звук включен)
is_muted = volume.GetMute()
print(f"Звук выключен: {is_muted}")

# Отключение/включение звука
volume.SetMute(0, None)  # 1 - выключить звук, 0 - включить звук
