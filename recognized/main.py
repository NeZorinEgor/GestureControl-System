import cv2
from recognized.src.measurements import (process_hand_landmarks,
                                         is_up_finger, change_moods_and_log_state)
from datetime import datetime, timedelta
from config import (logs, hand_points, up_fingers, finger_start_times, all_fingers_bent_time,
                    distance_mode, print_fingers_mode, print_coordinate_mode, previous_distance,
                    mp_hand, hands, mp_draw, camera)

from recognized.src.logic import start
from recognized.src.visualization import show

# start()
# show()
start(print_fingers_mode=True)



