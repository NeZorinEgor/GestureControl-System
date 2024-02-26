import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils


def calculate_distance_between_finger(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_hand_distance(hand_landmark, focal_length=1000):
    """
        Функция для получения расстояния от руки до камеры
        :param hand_landmark:
        :param focal_length: фокусное расстояние камеры (может потребоваться калибровка)
        :return: расстояния от руки до камеры
    """
    # Ширина ладони в метрах (примерное значение)
    hand_width_meters = 0.05

    # Размер ладони на изображении (пиксели)
    hand_width_pixels = calculate_distance_between_finger(hand_landmark[0][0], hand_landmark[0][1],
                                                          hand_landmark[1][0],
                                                          hand_landmark[1][1])

    # Формула подобия треугольников
    return (hand_width_meters * focal_length) / hand_width_pixels


def process_hand_landmarks(image, hand_landmarks):
    mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    x1, y1 = get_coordinate(hand_landmarks, 8, image)
    x2, y2 = get_coordinate(hand_landmarks, 4, image)

    distance = calculate_distance_between_finger(x1, y1, x2, y2)
    distance_str = "{:.2f}".format(distance)

    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, distance_str, (int((x1 + x2) / 2), int((y1 + y2) / 2) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    distance_to_camera = calculate_hand_distance([(x1, y1), (x2, y2)])
    cv2.putText(image, f'Distance to camera: {distance_to_camera:.2f} meters', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return distance


def get_coordinate(hand_landmark, index, image):
    return int(hand_landmark.landmark[index].x * image.shape[1]), int(hand_landmark.landmark[index].y * image.shape[0])


