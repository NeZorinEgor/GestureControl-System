import cv2
import mediapipe as mp

logs = True
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture("http://192.168.43.51:81/stream")


# mediapipe hand settings
mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_draw = mp.solutions.drawing_utils

hand_points = [0 for point_id in range(21)]        # list of point id
up_fingers = [0 for finger in range(4)]            # list of fingertip
finger_start_times = {i: None for i in range(4)}   # time when the finger was first detected up
all_fingers_bent_time = None                       # time when all fingers were first detected bent
distance_mode = False  # flag for distance measurement mode
print_fingers_mode = False                         # flag for print fingers mode
print_coordinate_mode = False                      # flag for print coordinate mode
previous_distance = None                           # Initialize previous distance as None
