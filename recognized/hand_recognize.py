import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1)

cap = cv2.VideoCapture(0)

tip_ids = [8, 12, 16, 20]
base_ids = [5, 9, 13, 17]
extension_threshold = 0.17


def get_vector(p1, p2):
    return np.array([p2.x - p1.x, p2.y - p1.y, p2.z - p1.z])


def is_finger_extended(base, tip, is_thumb=False):
    base_to_tip = get_vector(base, tip)
    base_to_tip_norm = np.linalg.norm(base_to_tip)
    return base_to_tip_norm > extension_threshold


while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_height, frame_width, _ = frame.shape

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS)
            landmarks = np.array([(lm.x * frame_width, lm.y * frame_height) for lm in hand_landmarks.landmark],
                                 dtype=np.int32)
            if len(landmarks) > 0:
                # Calculate hand area
                hand_area = cv2.contourArea(landmarks)
                # Calculate percentage of hand area in frame
                hand_area_percent = (hand_area / (frame_width * frame_height)) * 100
                # Display hand area percentage
                cv2.putText(frame, f'Hand Size: {hand_area_percent:.2f}%', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
                # Draw polygon around hand
                cv2.drawContours(frame, [landmarks], -1, (0, 255, 0), 2)
                # Display hand area percentage as a number near hand
                min_x, max_x = landmarks[:, 0].min(), landmarks[:, 0].max()
                min_y, max_y = landmarks[:, 1].min(), landmarks[:, 1].max()
                cv2.putText(frame, f'{hand_area_percent:.2f}%', (max_x + 10, max_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)

        if hand_landmarks:
            landmarks = hand_landmarks.landmark
            fingers_status = []
            for finger_index, tip_id in enumerate(tip_ids):
                base_id = base_ids[finger_index]
                if is_finger_extended(landmarks[base_id], landmarks[tip_id]):
                    fingers_status.append(1)
                else:
                    fingers_status.append(0)

            # Display the binary representation of fingers status
            status_str = ' '.join(map(str, fingers_status))
            cv2.putText(frame,
                        status_str,
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2)

    cv2.imshow('Fingers', frame)

    if cv2.waitKey(10) == 27:
        break

cap.release()
cv2.destroyAllWindows()

