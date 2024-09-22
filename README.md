# Face-Recognition-Based-Attendance-System
## Overview
This project is a **Face Recognition-Based Login, Logout, and User Registration System** developed using **Python**, **Tkinter** (for the GUI), and **OpenCV** (for image processing and face recognition). It allows users to register their face, log in, and log out by detecting their face through the webcam. All login attempts are logged with timestamps and save the photo taken at the time of registeration in a database.

## Features
- **Real-time Face Recognition**: Detects faces using a webcam and authenticates users.
- **Login/Logout System**: Users can log in and log out using their facial data.
- **User Registration**: New users can register their face, which is stored for future login/logout authentication.
- **Attendance Logging**: Automatically logs user login and logout with timestamps.
- **GUI**: Built with Tkinter for an intuitive and user-friendly experience.

## Technologies Used
- **Python**: Core programming language.
- **OpenCV**: For capturing and processing images from the webcam and performing face recognition.
- **Tkinter**: For creating the graphical user interface.
- **PIL (Pillow)**: For handling image display in the GUI.
- **face_recognition**: Python library for face recognition.

## Requirements
To run this project, you'll need the following libraries installed:

```bash
pip install opencv-python
pip install pillow
pip install face_recognition
