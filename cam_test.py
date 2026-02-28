import cv2

# open laptop camera (0 = default webcam)
camera = cv2.VideoCapture(0)

# check if camera opened
if not camera.isOpened():
    print("Camera not detected!")
    exit()

print("Camera working. Press ESC to exit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Failed to capture frame")
        break

    # show camera window
    cv2.imshow("Camera Test", frame)

    # press ESC key to close
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()