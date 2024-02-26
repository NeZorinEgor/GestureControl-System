import cv2
from hand_cv import HandRecognized


def main():
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = HandRecognized.hands_detector.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                HandRecognized.process_hand_landmarks(frame, hand_landmarks)

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
