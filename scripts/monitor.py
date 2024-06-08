import screen_brightness_control as sbc
import sys

# Получение параметров командной строки
params = sys.argv[1:]  # Первым элементом в sys.argv является имя скрипта
force = int(params[-1])

# Получение текущего уровня яркости
current_brightness = sbc.get_brightness(display=0)
#print(f"Текущая яркость: {current_brightness}%")

# Установка яркости (значение от 0 до 100)
sbc.set_brightness(force, display=1)  # Установить яркость на 50%
