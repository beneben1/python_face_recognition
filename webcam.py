import cv2
import numpy as np
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
import face_recognition

# Define the main application class
class MyFaceRecognitionApp(App):
    def build(self):
        # Initialize the camera capture
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Error: Camera not found or cannot be opened.")
            return

        # Create Kivy widgets for displaying the camera feed, labels, and buttons
        self.img = Image()
        self.name_label = Label(text="Name: Unknown", font_size=20)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.img)
        layout.add_widget(self.name_label)
        self.capture_button = Button(text="Capture Photo")
        self.capture_button.bind(on_press=self.capture_photo)
        layout.add_widget(self.capture_button)
        self.register_with_photo_button = Button(text="Register with Photo")
        self.register_with_photo_button.bind(on_press=self.register_with_photo)
        layout.add_widget(self.register_with_photo_button)
        self.login_button = Button(text="Login with Face")
        self.login_button.bind(on_press=self.login_with_face)
        layout.add_widget(self.login_button)

        # Create a connection to the SQLite database
        self.db_connection = sqlite3.connect("face_recognition.db")
        self.create_table_if_not_exists()
        self.registered_name = None
        self.registered_face_encoding = None

        # Load Haar Cascade Classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.captured_photo = None
        return layout

    # Create a database table if it doesn't exist
    def create_table_if_not_exists(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS faces
                        (name TEXT, encoding BLOB, photo BLOB)''')
        self.db_connection.commit()

    # Capture a photo from the camera
    def capture_photo(self, instance):
        ret, frame = self.capture.read()
        if ret:
            self.captured_photo = frame
            self.display_image(frame)
            print("Photo captured")

    # Display an OpenCV image in the Kivy widget
    def display_image(self, frame):
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

    # Register a face with a captured photo
    def register_with_photo(self, instance):
        if self.captured_photo is not None:
            detected_face = self.detect_face(self.captured_photo)
            if detected_face is not None:
                name = "bendavidi"  # Replace with the actual name
                self.name_label.text = f"Name: {name}"
                self.save_face_to_db(name, detected_face)
                print(f"Face registered as '{name}'")
                self.registered_name = name
                self.registered_face_encoding = self.encode_face(detected_face)
            else:
                self.name_label.text = "Name: Unknown"
                print("Face not recognized. Please try again.")
        else:
            self.name_label.text = "Name: Unknown"
            print("Capture a photo first.")

    # Login using face recognition
    def login_with_face(self, instance):
        if self.captured_photo is not None:
            detected_face = self.detect_face(self.captured_photo)
            if detected_face is not None and self.registered_name is not None and self.registered_face_encoding is not None:
                detected_face_rgb = cv2.cvtColor(detected_face, cv2.COLOR_BGR2RGB)  # Convert to RGB
                if self.match_face(detected_face_rgb, self.registered_face_encoding):
                    self.name_label.text = f"Welcome, {self.registered_name}!"
                    print(f"Welcome, {self.registered_name}!")
                    self.display_image(detected_face_rgb)  # Display the recognized face
                else:
                    self.name_label.text = "Name: Unknown"
                    print("Face not recognized. Please try again.")
            else:
                self.name_label.text = "Name: Unknown"
                print("No registered face found.")
        else:
            self.name_label.text = "Name: Unknown"
            print("Capture a photo first.")

    # Detect a face in the given frame using Haar Cascade Classifier
    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            x, y, w, h = faces[0]
            detected_face = gray[y:y + h, x:x + w]
            return detected_face
        return None

    # Encode a detected face using face_recognition library
    def encode_face(self, detected_face):
        detected_face_rgb = cv2.cvtColor(detected_face, cv2.COLOR_BGR2RGB)
        detected_face_encoding = face_recognition.face_encodings(detected_face_rgb)
        if len(detected_face_encoding) > 0:
            encoding_str = detected_face_encoding[0].tostring()
            return encoding_str
        return None

    # Match a detected face with a registered face encoding
    def match_face(self, detected_face, registered_face_encoding):
        detected_face_encoding = face_recognition.face_encodings(detected_face)
        if len(detected_face_encoding) > 0:
            distance = np.linalg.norm(
                np.frombuffer(registered_face_encoding, dtype=np.float64) - detected_face_encoding[0])
            threshold = 0.6  # Adjust the threshold as needed
            if distance < threshold:
                return True
        return False

    # Save a registered face to the SQLite database
    def save_face_to_db(self, name, detected_face):
        encoding_str = self.encode_face(detected_face)
        if encoding_str is not None:
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO faces VALUES (?, ?, ?)",
                        (name, sqlite3.Binary(encoding_str), sqlite3.Binary(detected_face.tobytes())))
            self.db_connection.commit()

    # Release the camera and close the database connection when the app stops
    def on_stop(self):
        self.capture.release()
        self.db_connection.close()

# Run the app if the script is executed directly
if __name__ == "__main__":
    MyFaceRecognitionApp().run()
