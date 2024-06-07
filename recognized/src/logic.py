
import cv2
import time
from recognized.src.measurements import (process_hand_landmarks,
                                         is_up_finger, change_moods_and_log_state)
from datetime import datetime, timedelta
from recognized.config import (logs, mp_hand, hands, mp_draw, camera)

distance_mode = True

def start(all_fingers_bent_time=None, distance_mode=False, print_fingers_mode=False,
         print_coordinate_mode=False, previous_distance=None, min_duration=1):

    hand_points = [0 for point_id in range(21)]  # list of point id
    up_fingers = [0 for finger in range(4)]  # list of fingertip
    last_state = up_fingers.copy()
    finger_start_times = {i: None for i in range(4)}  # time when the finger was first detected up

    start_time = time.time()
    while camera.isOpened():
        now_time = time.time()
        if now_time - start_time >= min_duration:
            start_time = now_time
            send_flag = True
        else:
            send_flag = False
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

                # Check up fingers
                is_up_finger(hand_points, 5, 8, 0, up_fingers)  # Index finger
                is_up_finger(hand_points, 9, 12, 1, up_fingers)  # Middle finger
                is_up_finger(hand_points, 13, 16, 2, up_fingers)  # Ring finger
                is_up_finger(hand_points, 17, 20, 3, up_fingers)  # Little finger

                # Check finger uptime and set mode
                now = datetime.now()

                if up_fingers.count(True) == 4:
                    if all_fingers_bent_time is None:
                        all_fingers_bent_time = now
                    elif now - all_fingers_bent_time >= timedelta(seconds=0.5):
                        # distance_mode = False
                        # print_fingers_mode = False
                        # print_coordinate_mode = False
                        if logs:
                            print("All fingers have been bent for 3 seconds, exiting all modes")
                        all_fingers_bent_time = None
                else:
                    all_fingers_bent_time = None

                # Set mod's
                if distance_mode and not print_coordinate_mode:
                    current_distance = process_hand_landmarks(frame, hand_lms)
                    if previous_distance is not None:
                        if logs:
                            if current_distance > previous_distance:
                                print(True)
                            else:
                                print(False)
                    previous_distance = current_distance

                if print_fingers_mode:
                    if logs and send_flag and (up_fingers != last_state):
                        last_state = up_fingers.copy()

                        print("Printing up_fingers:", up_fingers, last_state)

                if print_coordinate_mode:
                    finger_start_times[0] = None
                    if logs:
                        print(hand_lms.landmark[8])
