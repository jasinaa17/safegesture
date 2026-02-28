import winsound
import smtplib
from email.message import EmailMessage
import cv2
from datetime import datetime
import os
#screenshot to email
SENDER_EMAIL = "blinksense02@gmail.com"
APP_PASSWORD = "owyqjokwnizocogv"
RECEIVER_EMAIL = "jessyyyy17@gmail.com"
#beep
def beep():
    winsound.Beep(1000, 700)
#savingthess
def save_screenshot(frame):
    filename = f"screenshots/alert_{datetime.now().strftime('%H%M%S')}.jpg"
    cv2.imwrite(filename, frame)
    return filename
#sending the mail
def send_email(image_path, label):
    msg = EmailMessage()
    msg["Subject"] = f"SAFEGESTURE ALERT: {label.upper()} DETECTED"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(
        f"Distress gesture detected: {label}\nImmediate attention required."
    )
    with open(image_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="image",
            subtype="jpeg",
            filename="alert.jpg"
        )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
    print("The Email is sent successfully!")