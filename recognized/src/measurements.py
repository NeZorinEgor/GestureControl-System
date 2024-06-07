import math
import cv2

import recognized.config
from recognized.config import (mp_hand,
                               mp_draw)

up_fingers = recognized.config.up_fingers


def calculate_distance_between_finger(x1, y1, x2, y2):
    """ Вычисляет расстояние между двумя точками """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_coordinate(hand_landmark, index, image):
    """ Получает координаты точки (index) руки (hand_landmark) на изображении (image). """
    return int(hand_landmark.landmark[index].x * image.shape[1]), int(hand_landmark.landmark[index].y * image.shape[0])



def process_hand_landmarks(image, hand_landmarks):
    """
    Обрабатывает и рисует координаты рук на изображении (image).
    Возвращает расстояние между кончиком указательного пальца и большим пальцем.
    """
    mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)
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



def is_up_finger(points, hand_center_id, fingertip_id, finger_in_list_id, up_fingers):
    """
    `Finger is up? 1 : 0`
    Логика определения:
        Если расстояние от WRIST (запястье, 0 точка) до точки начала пальца
        (INDEX_FINGER [5, 9, 13, 17]) больше, чем расстояние от точки начала пальца
        (INDEX_FINGER [5, 9, 13, 17]) до кончика пальца, то палец согнут.
    """
    distance_0_to_hand_center = abs(points[0] - points[hand_center_id])
    distance_0_to_fingertip = abs(points[0] - points[fingertip_id])
    distance_good = distance_0_to_hand_center + (distance_0_to_hand_center / 2)
    if distance_0_to_fingertip > distance_good:
        up_fingers[finger_in_list_id] = True
    else:
        up_fingers[finger_in_list_id] = False



def change_moods_and_log_state(dist_m: bool, pr_f_m: bool, pr_coord_m: bool):
    """ Смена состояния программы и её логирование """
    global distance_mode, print_fingers_mode, print_coordinate_mode
    distance_mode = dist_m
    print_fingers_mode = pr_f_m
    print_coordinate_mode = pr_coord_m
    #  Log state
    if dist_m: print("Index finger has been up for 3 seconds, entering distance measurement mode")
    if pr_f_m: print(f"Little finger has been up for 3 seconds, entering print fingers mode\n{up_fingers}")
    if pr_coord_m: print("Middle finger has been up for 3 seconds, entering print index finger coordinates mode")


