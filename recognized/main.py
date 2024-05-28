import cv2
import mediapipe as mp
from datetime import datetime, timedelta

# read web-camera / streem from ESP-32
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture("http://172.20.10.8:81/streem")

# mediapipe hand settings
mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_draw = mp.solutions.drawing_utils

# list of poit id
hand_points = [0 for point_id in range(21)]

# list of fingertip
up_fingers = [0 for finger in range(4)]

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


# time when the finger was first detected up
finger_start_times = {i: None for i in range(4)}


while camera.isOpened():
    # Read frame
    _, frame = camera.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw hand
    result = hands.process(frame_rgb)
    if result.multi_hand_landmarks:
        for hand_lms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_lms, mp_hand.HAND_CONNECTIONS)
            # Work with hand point. See https://www.researchgate.net/publication/357216549/figure/fig2/AS:1103448439304192@1640094017201/Hand-Landmark-in-MediaPipe-38.ppm
            for point_id, point_coordinates in enumerate(hand_lms.landmark):
                width, height, color = frame.shape
                width, height = int(point_coordinates.x * height), int(point_coordinates.y * width)
                hand_points[point_id] = height
                # Draw color point at frame
                match point_id:
                    case 8: cv2.circle(frame, (width, height), 15, (0, 0, 255), cv2.FILLED)        # Index finger
                    case 12: cv2.circle(frame, (width, height), 15, (0, 255, 0), cv2.FILLED)       # Middle finger
                    case 16: cv2.circle(frame, (width, height), 15, (255, 0, 0), cv2.FILLED)       # Ring finder
                    case 20: cv2.circle(frame, (width, height), 15, (255, 255, 255), cv2.FILLED)   # Little finger

            is_up_finger(hand_points, 5, 8, 0)
            is_up_finger(hand_points, 9, 12, 1)
            is_up_finger(hand_points, 13, 16, 2)
            is_up_finger(hand_points, 17, 20, 3)
            # print(up_fingers)

            now = datetime.now()
            for i, finger_up in enumerate(up_fingers):
                if finger_up:
                    if finger_start_times[i] is None:
                        finger_start_times[i] = now
                    elif now - finger_start_times[i] >= timedelta(seconds=3):
                        match i:
                            case 0: print("Index finger has been up for 3 seconds")
                            case 1: print("Middle finger has been up for 3 seconds")
                            case 2: print("Ring finger has been up for 3 seconds")
                            case 3: print("Little finger has been up for 3 seconds")
                        # reset finger_start_time if needed
                        finger_start_times[i] = None
                else:
                    finger_start_times[i] = None

    # Draw frame
    cv2.imshow('frame', frame)

    # Close window
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
