import cv2
from datetime import datetime, timedelta

from recognized.measurements import is_up_finger, process_hand_landmarks
from recognized.config import (mp_hand,
                               hands,
                               mp_draw,
                               hand_points,
                               up_fingers,
                               finger_start_times,
                               all_fingers_bent_time,
                               distance_mode,
                               print_fingers_mode,
                               print_coordinate_mode,
                               previous_distance)


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
                    case 8:
                        cv2.circle(frame, (width, height), 15, (0, 0, 255), cv2.FILLED)  # Index finger
                    case 12:
                        cv2.circle(frame, (width, height), 15, (0, 255, 0), cv2.FILLED)  # Middle finger
                    case 16:
                        cv2.circle(frame, (width, height), 15, (255, 0, 0), cv2.FILLED)  # Ring finger
                    case 20:
                        cv2.circle(frame, (width, height), 15, (255, 255, 255), cv2.FILLED)  # Little finger

            # Check up fingers
            is_up_finger(hand_points, 5, 8, 0)  # Index finger
            is_up_finger(hand_points, 9, 12, 1)  # Middle finger
            is_up_finger(hand_points, 13, 16, 2)  # Ring finger
            is_up_finger(hand_points, 17, 20, 3)  # Little finger

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
                                print(
                                    "Middle finger has been up for 3 seconds, entering print index finger coordinates mode")

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
