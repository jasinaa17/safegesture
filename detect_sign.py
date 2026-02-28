import cv2
import mediapipe as mp
import joblib
import time
import threading
from alert_system import beep, save_screenshot, send_email
#training
model = joblib.load("model/gesture_model.pkl")
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)
#redoverlay
def red_alert_overlay(frame):
    overlay = frame.copy()
    cv2.rectangle(
        overlay,
        (0, 0),
        (frame.shape[1], frame.shape[0]),
        (0, 0, 255),
        -1
    )
    alpha = 0.35
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    return frame
#sendmail
def send_alert_async(image_path, prediction):
    threading.Thread(
        target=send_email,
        args=(image_path, prediction),
        daemon=True
    ).start()
last_alert_time = 0
cooldown = 3
while True:
    ret, frame = cap.read()
    if not ret:
        break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        data = []
        for lm in landmarks.landmark:
            data.extend([lm.x, lm.y, lm.z])
        prediction = model.predict([data])[0]
        cv2.putText(frame, prediction.upper(),
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),3)
#criticalordostreess word
        if prediction in ["help", "sos"]:
            frame = red_alert_overlay(frame)
            cv2.putText(frame,
                        f"!!! {prediction.upper()} DETECTED !!!",
                        (50,100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (255,255,255),
                        3)
            current_time = time.time()
            if current_time - last_alert_time > cooldown:
                beep()
                image_path = save_screenshot(frame)
                send_alert_async(image_path, prediction)
                last_alert_time = current_time
    cv2.imshow("SAFEGESTURE Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()