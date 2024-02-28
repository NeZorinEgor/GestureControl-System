import cv2
import serial
from cv.hand_cv.HandRecognized import process_hand_landmarks, hands_detector

PORT = 'COM9'
BAUD_RATE = 9600


def main():
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        print(f"Ошибка открытия порта: {e}")
        return

    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands_detector.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                confidence_score = process_hand_landmarks(frame, hand_landmarks)
                if confidence_score > 80:
                    ser.write(b'1')
                else:
                    ser.write(b'0')

        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    ser.close()


if __name__ == '__main__':
    main()