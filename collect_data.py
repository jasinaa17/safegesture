import cv2
import mediapipe as mp
import os
import time

save_path = f"dataset/{label}"
os.makedirs(save_path, exist_ok=True)

#hand_detection

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
#camera_detection
cap = cv2.VideoCapture(0)

count = 0
last_capture_time = 0
capture_delay = 0.5   # seconds between captures

print("Show gesture. Press ESC to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
        current_time = time.time()
        if current_time - last_capture_time > capture_delay:
            filename = f"{save_path}/{count}.jpg"
            cv2.imwrite(filename, frame)
            last_capture_time = current_time
            print("Saved:", count)
    cv2.putText(frame,
                f"Label: {label} | Images: {count}",
                (10,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.imshow("Collecting Data", frame)
 #>200
    if cv2.waitKey count >= 200:
        break
cap.release()
cv2.destroyAllWindows()