    import cv2
    import mediapipe as mp
    import numpy as np

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('http://172.0.0.1:8080/streem')

    tip_ids = [8, 12, 16, 20]
    base_ids = [5, 9, 13, 17]
    extension_threshold = 0.17


    def get_vector(p1, p2):
        return np.array([p2.x - p1.x, p2.y - p1.y, p2.z - p1.z])


    def is_finger_extended(base, tip, is_thumb=False):
        base_to_tip = get_vector(base, tip)
        base_to_tip_norm = np.linalg.norm(base_to_tip)
        return base_to_tip_norm > extension_threshold


    def calculate_distance_and_draw_line(image):
        """
        Функция для вычисления расстояния между большим и указательным пальцами на изображении.
        Рисует линию между пальцами и возвращает изображение с нанесенной линией и расстояние между пальцами.
        """
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        distance = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = image.shape
                thumb_tip_coords = np.array([thumb_tip.x * w, thumb_tip.y * h])
                index_finger_tip_coords = np.array([index_finger_tip.x * w, index_finger_tip.y * h])
                distance = np.linalg.norm(thumb_tip_coords - index_finger_tip_coords)
                cv2.line(image, tuple(thumb_tip_coords.astype(int)), tuple(index_finger_tip_coords.astype(int)), (255, 0, 0), 3)
                cv2.putText(image, f'Distance: {int(distance)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        return image, distance


    while True:
        _, frame = cap.read()
        frame_height, frame_width, _ = frame.shape

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = np.array([(lm.x * frame_width, lm.y * frame_height) for lm in hand_landmarks.landmark],
                                     dtype=np.int32)
                if len(landmarks) > 0:
                    hand_area = cv2.contourArea(landmarks)
                    hand_area_percent = (hand_area / (frame_width * frame_height)) * 100
                    cv2.putText(frame, f'Hand Size: {hand_area_percent:.2f}%', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255), 2)
                    min_x, max_x = landmarks[:, 0].min(), landmarks[:, 0].max()
                    min_y, max_y = landmarks[:, 1].min(), landmarks[:, 1].max()
                    cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)
                    cv2.putText(frame, f'{hand_area_percent:.2f}%', (max_x + 10, max_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255), 2)

                landmarks_list = hand_landmarks.landmark
                fingers_status = []
                for finger_index, tip_id in enumerate(tip_ids):
                    base_id = base_ids[finger_index]
                    if is_finger_extended(landmarks_list[base_id], landmarks_list[tip_id]):
                        fingers_status.append(1)
                    else:
                        fingers_status.append(0)

                # Display the binary representation of fingers status
                status_str = ' '.join(map(str, fingers_status))
                cv2.putText(frame, status_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                print(f"{status_str}")

        cv2.imshow('Fingers', frame)

        if cv2.waitKey(10) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
