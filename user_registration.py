import os
import cv2
import face_recognition
from tkinter import simpledialog
from constants import IMAGES_FOLDER
from database import insert_user

def register_user_with_gui():
    user_name = simpledialog.askstring("User Registration", "Enter user's name:")
    if user_name:
        user_folder = os.path.join(IMAGES_FOLDER, user_name)
        os.makedirs(user_folder, exist_ok=True)
        
        print("Press 'q' to capture an image. Press 'e' to finish.")
        
        cap = cv2.VideoCapture(0)
        count = 0
        encodings = []  # Store face encodings for all captured images
        
        while True:
            ret, frame = cap.read()
            cv2.imshow('Capture', frame)
            
            # Press 'q' to capture image
            if cv2.waitKey(1) & 0xFF == ord('q'):
                image_path = os.path.join(user_folder, f'{count}.jpg')
                cv2.imwrite(image_path, frame)
                print(f"Image {count} captured.")
                count += 1
            
            elif cv2.waitKey(1) & 0xFF == ord('e'):  # Press 'e' to finish
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Encode the user's face images if at least one image is captured
        if count > 0:
            # Encode the user's face images
            user_images = [os.path.join(user_folder, img) for img in os.listdir(user_folder)]
            encodings = []

            for img_path in user_images:
                image = face_recognition.load_image_file(img_path)
                encoding_list = face_recognition.face_encodings(image)
                if encoding_list:
                    encoding = encoding_list[0]
                    encodings.append(encoding)

            # Store the user's information in the database
            insert_user(user_name, encodings)
            print(f"{user_name} has been registered successfully.")
        else:
            print("No face detected in the captured images. Registration canceled.")
    else:
        print("Registration canceled.")
