import cv2
import mediapipe as mp
from datetime import datetime, timedelta
import math

# mediapipe hand settings
mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_draw = mp.solutions.drawing_utils

hand_points = [0 for point_id in range(21)]        # list of point id
up_fingers = [0 for finger in range(4)]            # list of fingertip
finger_start_times = {i: None for i in range(4)}   # time when the finger was first detected up
all_fingers_bent_time = None                       # time when all fingers were first detected bent
distance_mode = False                              # flag for distance measurement mode
print_fingers_mode = False                         # flag for print fingers mode
print_coordinate_mode = False                      # flag for print coordinate mode
previous_distance = None                           # Initialize previous distance as None


def calculate_distance_between_finger(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_coordinate(hand_landmark, index, image):
    return int(hand_landmark.landmark[index].x * image.shape[1]), int(hand_landmark.landmark[index].y * image.shape[0])


def process_hand_landmarks(image, hand_landmarks):
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


def is_up_finger(points, hand_center_id, fingertip_id, finger_in_list_id):
    """
    `Finger is up? 1 : 0`
    Логика определения:
        Если расстояние от WRIST (запястье, 0 точка) до точки начала пальца
        (INDEX_FINGER [5, 9, 13, 17]) больше, чем расстояние от точки начала пальца
        (INDEX_FINGER [5, 9, 13, 17]) до кончика пальца, то палец согнут.
    """
    global up_fingers
    distance_0_to_hand_center = abs(points[0] - points[hand_center_id])
    distance_0_to_fingertip = abs(points[0] - points[fingertip_id])
    distance_good = distance_0_to_hand_center + (distance_0_to_hand_center / 2)
    if distance_0_to_fingertip > distance_good:
        up_fingers[finger_in_list_id] = True
    else:
        up_fingers[finger_in_list_id] = False

# read web-camera / stream from ESP-32
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture("http://172.20.10.8:81/stream")

while camera.isOpened():
    # Read frame
    _, frame = camera.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw hand
    result = hands.process(frame_rgb)
    if result.multi_hand_landmarks:
        for hand_lms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_lms, mp_hand.HAND_CONNECTIONS)

            # Work with hand points
            for point_id, point_coordinates in enumerate(hand_lms.landmark):
                width, height, color = frame.shape
                width, height = int(point_coordinates.x * height), int(point_coordinates.y * width)
                hand_points[point_id] = height

                # Draw color point at frame
                match point_id:
                    case 8: cv2.circle(frame, (width, height), 15, (0, 0, 255), cv2.FILLED)        # Index finger
                    case 12: cv2.circle(frame, (width, height), 15, (0, 255, 0), cv2.FILLED)       # Middle finger
                    case 16: cv2.circle(frame, (width, height), 15, (255, 0, 0), cv2.FILLED)       # Ring finger
                    case 20: cv2.circle(frame, (width, height), 15, (255, 255, 255), cv2.FILLED)   # Little finger

            # Check up fingers
            is_up_finger(hand_points, 5, 8, 0)     # Index finger
            is_up_finger(hand_points, 9, 12, 1)    # Middle finger
            is_up_finger(hand_points, 13, 16, 2)   # Ring finger
            is_up_finger(hand_points, 17, 20, 3)   # Little finger

            # Check finger uptime and set mode
            now = datetime.now()
            for i, finger_up in enumerate(up_fingers):
                if finger_up:
                    if finger_start_times[i] is None:
                        finger_start_times[i] = now
                    elif now - finger_start_times[i] >= timedelta(seconds=3):
                        if up_fingers.count(True) == 1:
                            if i == 0:
                                distance_mode = True
                                print_fingers_mode = False
                                print_coordinate_mode = False
                                print("Index finger has been up for 3 seconds, entering distance measurement mode")
                            elif i == 3:
                                print_fingers_mode = True
                                distance_mode = False
                                print_coordinate_mode = False
                                print("Little finger has been up for 3 seconds, entering print fingers mode")
                                print(up_fingers)
                            elif i == 1:
                                print_coordinate_mode = True
                                print_fingers_mode = False
                                distance_mode = False
                                print("Middle finger has been up for 3 seconds, entering print index finger coordinates mode")

                        finger_start_times[i] = None
                else:
                    finger_start_times[i] = None

            if up_fingers.count(True) == 0:
                if all_fingers_bent_time is None:
                    all_fingers_bent_time = now
                elif now - all_fingers_bent_time >= timedelta(seconds=3):
                    distance_mode = False
                    print_fingers_mode = False
                    print_coordinate_mode = False
                    print("All fingers have been bent for 3 seconds, exiting all modes")
                    all_fingers_bent_time = None
            else:
                all_fingers_bent_time = None

            # Set mod`s
            if distance_mode and print_coordinate_mode != True:
                current_distance = process_hand_landmarks(frame, hand_lms)
                if previous_distance is not None:
                    if current_distance > previous_distance:
                        print(True)
                    else:
                        print(False)
                previous_distance = current_distance

            if print_fingers_mode:
                print("Printing up_fingers:", up_fingers)

            if print_coordinate_mode:
                distance_mode = False
                finger_start_times[0] = None
                print(hand_lms.landmark[8])

    # Draw image
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Close window
camera.release()
cv2.destroyAllWindows()


