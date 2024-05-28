import cv2
import mediapipe as mp

# read web-camera
camera = cv2.VideoCapture(0)
# read streem from ESP-32
# camera = cv2.VideoCapture("http://172.20.10.8:81/streem")

# mediapipe hand settings
mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_draw = mp.solutions.drawing_utils

# list of poit id
hand_points = [0 for point_id in range(21)]

up_fingers = [0 for finger in range(4)]

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

            # `Finger UP?` 1 : 0
            distance_0_5 = abs(hand_points[0] - hand_points[5])
            distance_0_8 = abs(hand_points[0] - hand_points[8])
            distance_good = distance_0_5 + (distance_0_5 / 2)
            if distance_0_8 > distance_good:
                up_fingers[0] = 1
            else:
                up_fingers[0] = 0

            print(up_fingers)

    # Draw frame
    cv2.imshow('frame', frame)

    # Close window
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
