import cv2
import serial
from hand_cv.HandRecognized import process_hand_landmarks, hands_detector

# Порт, к которому подключено Arduino
port = 'COM9'  # Измените на свой порт
baud_rate = 9600

# Создаем объект Serial
ser = serial.Serial(port, baud_rate, timeout=1)


def main():
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands_detector.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                process_hand_landmarks(frame, hand_landmarks)
                a = process_hand_landmarks(frame, hand_landmarks)
                if a > 80:
                    ser.write(b'1')  # Отправляем '1' на Arduino
                else:
                    ser.write(b'0')  # Отправляем '0' на Arduino

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    ser.close()  # Закрываем соединение после завершения программы


if __name__ == '__main__':
    main()
