# Face Recognition App

![App Screenshot][(screenshot.png)](https://github.com/beneben1/python_face_recognition/blob/77a400d3ccd9e39860ff8a3ba5f68b4a265fe604/screenshot.png)

## Overview

The Face Recognition App is a Python-based application that allows users to capture and register their faces using a webcam. It uses OpenCV for face detection, face_recognition for face encoding, and the Kivy framework for the user interface. Users can register their faces and later log in by recognizing their registered faces.

## Features

- Capture photos using your computer's webcam.
- Register your face with a name.
- Recognize and log in using your registered face.
- Store face data in an SQLite database.
- Simple and intuitive graphical user interface.

## Requirements

- Python 3.x
- OpenCV (cv2)
- numpy
- face_recognition
- sqlite3
- Kivy

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/yourusername/face-recognition-app.git
## Install the required Python packages:

shell
Copy code
pip install opencv-python numpy face_recognition kivy
Run the application:

-shell
-Copy code
-python main.py


## Usage
Launch the application.
Click the "Capture Photo" button to capture a photo using your webcam.
Click the "Register with Photo" button to register the captured face with a name.
Click the "Login with Face" button to recognize and log in using the registered face.
Database
The application uses an SQLite database (face_recognition.db) to store registered face data. You can manage the database using standard SQLite tools or libraries.

## Troubleshooting
If you encounter issues with the camera not working, ensure your webcam is connected and properly configured.
Adjust the recognition threshold in the code to fine-tune face recognition accuracy.
License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
This project uses the face_recognition library by Adam Geitgey.
Haar Cascade Classifier for face detection is part of OpenCV.
