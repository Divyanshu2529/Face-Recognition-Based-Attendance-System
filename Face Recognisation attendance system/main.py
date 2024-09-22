import datetime
import tkinter as tk
import util
import cv2
import os
import subprocess
from PIL import Image, ImageTk

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.configure(bg='white')

        # Login Button
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login, fg='black')
        self.login_button_main_window.place(x=750, y=200)

        # Register New User Button
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=280)

        # Logout Button
        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout, fg='black')
        self.logout_button_main_window.place(x=750, y=360)

        # Webcam Label
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)
        self.log_path = './attendance_log.txt'

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open webcam.")
                return

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            return
        
        self.most_recent_capture_arr = frame  # Store the raw frame (array)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        try:
            output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path])
            output = output.decode('utf-8')
            print(output)

            if 'unknown_person' in output:
                util.msg_box('Ups...', 'Unknown user. Please register as a new user or try again.')
            elif 'no_persons_found' in output:
                util.msg_box('No Person Found', 'There is something covering the face, No face detected.')
            else:
                name = output.split(',')[1].strip()
                util.msg_box('Welcome back!', f'Welcome, {name}.')
                with open(self.log_path, 'a') as f:
                    f.write(f'{name},{datetime.datetime.now()},in\n')
                    
        except FileNotFoundError as e:
            print(f"Error: {e}")

        finally:
            os.remove(unknown_img_path)

    def logout(self):
        unknown_img_path = './.tmp_logout.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        try:
            output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path])
            output = output.decode('utf-8')
            print(output)

            if 'unknown_person' in output:
                util.msg_box('Ups...', 'Unknown user. You never logged in.')
            elif 'no_persons_found' in output:
                util.msg_box('No Person Found', 'No face detected.')
            else:
                name = output.split(',')[1].strip()
                util.msg_box('Goodbye!', f'Goodbye, {name}.')
                with open(self.log_path, 'a') as f:
                    f.write(f'{name},{datetime.datetime.now()},out\n')

        except FileNotFoundError as e:
            print(f"Error: {e}")

        finally:
            os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x600+370+120")
        self.register_new_user_window.configure(bg='white')

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user, fg='black')
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user, fg='black')
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = tk.Entry(self.register_new_user_window, bg='white', fg='black', highlightbackground='black', highlightthickness=1, font=('Arial', 18))
        self.entry_text_register_new_user.place(x=750, y=150, width=250, height=50)

        self.text_label_register_new_user = tk.Label(self.register_new_user_window, text='Please, input \nusername:', bg='white', fg='black', font=('Arial', 30))
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        print("User registration accepted!")

        name = self.entry_text_register_new_user.get()

        cv2.imwrite(os.path.join(self.db_dir, f'{name}.jpg'), self.register_new_user_capture)

        util.msg_box('Success!', 'User registered successfully!')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()

