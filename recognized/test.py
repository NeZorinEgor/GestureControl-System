import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

previous_distance = None  # Initialize previous distance as None


def calculate_distance_between_finger(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def process_hand_landmarks(image, hand_landmarks):
    mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    x1, y1 = get_coordinate(hand_landmarks, 8, image)  # Index finger tip
    x2, y2 = get_coordinate(hand_landmarks, 4, image)  # Thumb tip

    distance = calculate_distance_between_finger(x1, y1, x2, y2)
    distance_str = "{:.2f}".format(distance)

    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.circle(image, (x1, y1), 10, (255, 0, 0), -1)
    cv2.circle(image, (x2, y2), 10, (255, 0, 0), -1)
    cv2.putText(image, distance_str, (int((x1 + x2) / 2), int((y1 + y2) / 2) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return distance


def get_coordinate(hand_landmark, index, image):
    return int(hand_landmark.landmark[index].x * image.shape[1]), int(hand_landmark.landmark[index].y * image.shape[0])


def main():
    global previous_distance  # Use the global variable to track previous distance
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands_detector.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                current_distance = process_hand_landmarks(frame, hand_landmarks)

                if previous_distance is not None:
                    if current_distance > previous_distance:
                        print(True)
                    else:
                        print(False)

                previous_distance = current_distance

        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
