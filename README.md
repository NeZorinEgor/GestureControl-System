# Дополняющий модуль к умному дому

Дополняющий модуль к умному дому на основе камеры, для определения жестов рук и возможность выставления команд на эти жесты(включить свет, регулировать яркость, открыть окно и т.д.)

##  Референсы
Запишу видос

## Схемы
Тут схема камеры или компонентов

## Cценарии  использования
Тут про подключение компонентов и Serial.read 
```cpp
void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600); 
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read(); 
    if (receivedChar == '1') {
      digitalWrite(13, HIGH); 
    } else if (receivedChar == '0') {
      digitalWrite(13, LOW); 
    }

  }
}
```

## Компоненты
Камера, esp, что-то про Wi-Fi

## Стек технологий

Машинное зрение:
* [OpenCV](https://opencv.org/)
* [Mediapipe](https://chuoling.github.io/mediapipe/solutions/hands.html)

Передача данных между компонентов:
* [Pyserial](https://github.com/pyserial/pyserial)
* mqtt?

Настольное приложение:
* [DearPyGUI](https://github.com/hoffstadt/DearPyGui)


