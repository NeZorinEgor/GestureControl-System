import cv2
import mediapipe as mp
from datetime import datetime, timedelta

# read web-camera / stream from ESP-32
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture("http://172.20.10.8:81/stream")

# mediapipe hand settings
mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_draw = mp.solutions.drawing_utils

hand_points = [0 for _ in range(21)]   # list of hand points
up_fingers = [0 for _ in range(4)]     # list of fingertip statuses

# dictionary to store the start time when a finger is detected up
finger_start_times = {i: None for i in range(4)}

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
                if point_id in [8, 12, 16, 20]:
                    color = (0, 0, 255) if point_id == 8 else (0, 255, 0) if point_id == 12 else (255, 0, 0) if point_id == 16 else (255, 255, 255)
                    cv2.circle(frame, (width, height), 15, color, cv2.FILLED)

            is_up_finger(hand_points, 5, 8, 0)
            is_up_finger(hand_points, 9, 12, 1)
            is_up_finger(hand_points, 13, 16, 2)
            is_up_finger(hand_points, 17, 20, 3)
            print(up_fingers)

            now = datetime.now()
            for finger_id, is_up in enumerate(up_fingers):
                if is_up:
                    if finger_start_times[finger_id] is None:
                        finger_start_times[finger_id] = now
                    elif now - finger_start_times[finger_id] >= timedelta(seconds=3):
                        print(f"Finger {finger_id} has been up for 3 seconds.")
                else:
                    finger_start_times[finger_id] = None

    # Draw frame
    cv2.imshow('frame', frame)

    # Close window
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
