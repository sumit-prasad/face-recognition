## Main Application (main.py):

Provides a graphical user interface (GUI) using tkinter.
Allows users to register new users, recognize users, reset the database, and exit the application.

## User Registration (user_registration.py):

Captures images from the camera to register new users.
Prompts the user for their name using a dialog.
Encodes and stores the captured user images and their name in a database.

## User Recognition (user_recognition.py):

Uses the camera to capture real-time video frames.
Recognizes and labels faces in the video stream.
Compares the recognized faces with known users' face encodings to identify them.

## Database Management (database.py):

Manages user data and storage.
Creates and maintains an SQLite database to store user information (names and face encodings).
Allows resetting the database with a security code, removing all user records and associated image data.


## Constants (constants.py):

Centralizes important constants used throughout the application, such as database file name, image folder, recognition threshold, and security code.
Overall, your Face Recognition System aims to register new users, recognize them in real-time using face recognition techniques, and provides database management functionality to reset the system if needed.