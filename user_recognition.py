import cv2
import face_recognition
from constants import THRESHOLD
from database import load_known_users

def recognize_user():
    # Initialize the camera capture
    video_capture = cv2.VideoCapture(0)

    # Load known user names and encodings
    known_names, known_encodings = load_known_users()

    while True:
        # Capture a frame from the camera
        ret, frame = video_capture.read()

        # Convert the frame to RGB format for face recognition
        rgb_frame = frame[:, :, ::-1]

        # Find face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the current face encoding with known encodings
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=THRESHOLD)
            name = "Unknown"  # Default to "Unknown" if no match found

            new_matches = []
            prev_element = None

            for element in matches:
                if element != prev_element:
                    new_matches.append(element)
                prev_element = element

            if any(new_matches):
                matched_index = new_matches.index(True)
                name = known_names[matched_index]

            # Draw a rectangle and label on the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Display the resulting image in real-time
        cv2.imshow('Face Recognition', frame)

        # Check for the 'q' key to exit the loop and close the window
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    # Release the video capture and close the OpenCV window
    video_capture.release()
    cv2.destroyAllWindows()
