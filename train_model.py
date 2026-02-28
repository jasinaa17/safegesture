import cv2
import mediapipe as mp
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

X = []
y = []

labels = ["help", "normal"]

for label in labels:
    folder = f"dataset/{label}"

    for file in os.listdir(folder):
        img = cv2.imread(f"{folder}/{file}")
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            data = []

            for lm in landmarks.landmark:
                data.extend([lm.x, lm.y, lm.z])

            X.append(data)
            y.append(label)

model = RandomForestClassifier()
model.fit(X, y)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/gesture_model.pkl")

print("Model trained and saved!")