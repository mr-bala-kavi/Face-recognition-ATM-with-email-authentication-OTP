import cv2

def capture_face(account_number):
    camera = cv2.VideoCapture(0)

    print("[INFO] Look at the camera to capture your face...")
    while True:
        ret, frame = camera.read()
        cv2.imshow("Capture Face (Press 's' to save)", frame)

        # Press 's' to save the image
        if cv2.waitKey(1) & 0xFF == ord('s'):
            image_path = f"faces/{account_number}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"[✅] Face image saved as: {image_path}")
            break

    camera.release()
    cv2.destroyAllWindows()

# Set your unique account number (as in accounts.csv)
account_number = input("Enter your account number: ")
capture_face(account_number)