import cv2
import os
import numpy as np
import face_recognition
import sqlite3
import shutil  # Import the shutil module for deleting folders
import tkinter as tk
from tkinter import simpledialog, messagebox


# Define paths and constants
DATABASE_FILE = "user_database.db"
IMAGES_FOLDER = "registered_users"
THRESHOLD = 0.6  # Adjust this threshold based on your application's needs
SECURITY_CODE = "1234"  # Set your security code

# Create the database table if it doesn't exist
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, encoding TEXT)''')
conn.commit()

# Create a new folder for user images if it doesn't exist
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# Function to capture and register a new user with a GUI
def register_user_with_gui():
    user_name = simpledialog.askstring("User Registration", "Enter user's name:")
    if user_name:
        user_folder = os.path.join(IMAGES_FOLDER, user_name)
        os.makedirs(user_folder, exist_ok=True)
        
        print("Press 'q' to capture an image. Press 'esc' to finish.")
        
        cap = cv2.VideoCapture(0)
        count = 0
        encodings = []  # Store face encodings for all captured images
        
        while True:
            ret, frame = cap.read()
            cv2.imshow('Capture', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                image_path = os.path.join(user_folder, f'{count}.jpg')
                cv2.imwrite(image_path, frame)
                print(f"Image {count} captured.")
                count += 1
            elif cv2.waitKey(1) & 0xFF == 27:  # Press 'esc' to finish
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Encode the user's face images
        user_images = [os.path.join(user_folder, img) for img in os.listdir(user_folder)]
        for img_path in user_images:
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)[0]
            encodings.append(encoding)
        
        # Convert face encodings to a string
        encoding_str = ",".join([",".join(map(str, encoding)) for encoding in encodings])
        
        # Store the user's information in the database
        cursor.execute("INSERT INTO users (name, encoding) VALUES (?, ?)", (user_name, encoding_str))
        conn.commit()
        print(f"{user_name} has been registered successfully.")


# Function to recognize users from the camera
def recognize_user():
    # Capture a frame from the camera
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    # Convert the frame to RGB format for face recognition
    rgb_frame = frame[:, :, ::-1]

    # Find face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        is_match = face_recognition.compare_faces(known_encodings, encoding, tolerance=THRESHOLD)
        name = "Unknown"  # Default to "Unknown" if no match found

        if any(is_match):
            matched_index = is_match.index(True)
            name = known_names[matched_index]

        # Draw a rectangle and label on the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Face Recognition', frame)
    cv2.waitKey(0)

    # Release the video capture and close the OpenCV window
    video_capture.release()
    cv2.destroyAllWindows()

# Function to reset the database and delete registered user data
def reset_database():
    security_code = simpledialog.askstring("Security Code", "Enter the security code to reset the database:")
    if security_code == SECURITY_CODE:
        confirm_reset = messagebox.askyesno("Reset Database", "Are you sure you want to reset the database?")
        if confirm_reset:
            # Delete all records from the database
            cursor.execute("DELETE FROM users")
            conn.commit()
            
            # Delete all user image folders
            for user_folder in os.listdir(IMAGES_FOLDER):
                user_folder_path = os.path.join(IMAGES_FOLDER, user_folder)
                if os.path.isdir(user_folder_path):
                    shutil.rmtree(user_folder_path)
            
            messagebox.showinfo("Database Reset", "Database reset completed.")
        else:
            messagebox.showinfo("Database Reset", "Database reset canceled.")
    else:
        messagebox.showwarning("Security Code Incorrect", "Security code is incorrect. Database reset canceled.")


# Function to exit the tkinter application
def exit_application():
    root.destroy()



# Create a GUI for user interaction
root = tk.Tk()
root.title("Face Recognition System")

# Load and display a background image
# background_img = Image.open("background.jpg")
# background_photo = ImageTk.PhotoImage(background_img)

# Configure grid columns and rows
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create a label for the background image
# background_label = tk.Label(root, image=background_photo)
# background_label.grid(row=0, column=0, rowspan=6, columnspan=3, sticky="nsew")

# Create labels and buttons with icons on top of the image
welcome_label = tk.Label(root, text="Welcome to Face Recognition System", font=("Helvetica", 16), bg='lightblue', pady=10, padx=10)
welcome_label.grid(row=1, column=1, pady=20)

# Create buttons with the same size
button_size = (10, 3)  # Adjust the size as needed
register_button = tk.Button(root, text="Register a new user", command=register_user_with_gui, padx=10, pady=5)
register_button.grid(row=2, column=1, pady=10, sticky="nsew")
register_button.config(width=button_size[0], height=button_size[1])

recognize_button = tk.Button(root, text="Recognize users", command=recognize_user, padx=10, pady=5)
recognize_button.grid(row=3, column=1, pady=10, sticky="nsew")
recognize_button.config(width=button_size[0], height=button_size[1])

reset_button = tk.Button(root, text="Reset Database", command=reset_database, padx=10, pady=5)
reset_button.grid(row=4, column=1, pady=10, sticky="nsew")
reset_button.config(width=button_size[0], height=button_size[1])

exit_button = tk.Button(root, text="Exit", command=root.destroy, padx=10, pady=5)
exit_button.grid(row=5, column=1, pady=10, sticky="nsew")
exit_button.config(width=button_size[0], height=button_size[1])

root.mainloop()

# Close the database connection
conn.close()
