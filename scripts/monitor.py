import screen_brightness_control as sbc

# Получение текущего уровня яркости
current_brightness = sbc.get_brightness(display=0)
print(f"Текущая яркость: {current_brightness}%")

# Установка яркости (значение от 0 до 100)
sbc.set_brightness(100, display=1)  # Установить яркость на 50%
