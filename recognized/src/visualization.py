from datetime import datetime, timedelta

import cv2

from recognized.config import (logs, mp_hand, hands, mp_draw, camera)
from recognized.src.measurements import (process_hand_landmarks,
                                         is_up_finger, change_moods_and_log_state)







def show(all_fingers_bent_time=None, distance_mode=False, print_fingers_mode=False,
         print_coordinate_mode=False, previous_distance=None):
    hand_points = [0 for point_id in range(21)]  # list of point id
    up_fingers = [0 for finger in range(4)]  # list of fingertip
    finger_start_times = {i: None for i in range(4)}  # time when the finger was first detected up

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

                    if logs:
                        # Draw color point at frame
                        match point_id:
                            case 8:
                                cv2.circle(frame, (width, height), 15, (0, 0, 255), cv2.FILLED)  # Index finger
                            case 12:
                                cv2.circle(frame, (width, height), 15, (0, 255, 0), cv2.FILLED)  # Middle finger
                            case 16:
                                cv2.circle(frame, (width, height), 15, (255, 0, 0), cv2.FILLED)  # Ring finger
                            case 20:
                                cv2.circle(frame, (width, height), 15, (255, 255, 255), cv2.FILLED)  # Little finger

                # Check up fingers
                is_up_finger(hand_points, 5, 8, 0, up_fingers)  # Index finger
                is_up_finger(hand_points, 9, 12, 1, up_fingers)  # Middle finger
                is_up_finger(hand_points, 13, 16, 2, up_fingers)  # Ring finger
                is_up_finger(hand_points, 17, 20, 3, up_fingers)  # Little finger

                # Check finger uptime and set mode
                now = datetime.now()
                for i, finger_up in enumerate(up_fingers):
                    if finger_up:
                        if finger_start_times[i] is None:
                            finger_start_times[i] = now
                        elif now - finger_start_times[i] >= timedelta(seconds=3):
                            if up_fingers.count(True) == 1:
                                match i:
                                    case 0:
                                        distance_mode, print_fingers_mode, print_coordinate_mode = True, False, False
                                    case 1:
                                        distance_mode, print_fingers_mode, print_coordinate_mode = False, False, True
                                    case 3:
                                        distance_mode, print_fingers_mode, print_coordinate_mode = False, True, False
                            finger_start_times[i] = None
                    else:
                        finger_start_times[i] = None

                if up_fingers.count(True) == 4:
                    if all_fingers_bent_time is None:
                        all_fingers_bent_time = now
                    elif now - all_fingers_bent_time >= timedelta(seconds=0.5):
                        distance_mode = False
                        print_fingers_mode = False
                        print_coordinate_mode = False
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
                    if logs:
                        print("Printing up_fingers:", up_fingers)
                    cv2.putText(frame, str(up_fingers), (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                if print_coordinate_mode:
                    finger_start_times[0] = None
                    if logs:
                        print(hand_lms.landmark[8])

        # Draw image
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    # Close window
    camera.release()
    cv2.destroyAllWindows()

