import os
import threading
import tkinter as tk
from tkinter import PhotoImage

import cv2
import sv_ttk
from tkcalendar import Calendar

from modules.apple import ICB
from modules.timestuff import *


class iCloudPhotoGrabber(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("iCloud Photo Grabber")
        self.geometry("300x400")

        self.extensions = {}

        self.iconbitmap(r'img\photo_icon.ico')

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # iCloud Login Frame
        self.login_frame = tk.Frame(self)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)

        # Username
        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        self.username_input = tk.Entry(self.login_frame)
        self.username_input.grid(row=1, column=0, pady=(0, 10))

        # Password
        tk.Label(self.login_frame, text="Password").grid(row=2, column=0)
        self.password_input = tk.Entry(self.login_frame, show="*")
        self.password_input.grid(row=3, column=0, pady=(0, 10))

        # Login buton
        tk.Button(self.login_frame, text="Login", command=self.login_to_icloud).grid(row=4, column=0, pady=10)

        # Calendar Button (Hidden))
        self.calendar_button = tk.Button(self, text="Select date", command=self.show_date_picker)

        # Loading gif (Hidden, lazy)
        self.loader_gif = 'img/loader.gif'
        num_frames = 20
        scale_factor = 2
        self.loader_frames = [
            PhotoImage(file=self.loader_gif, format=f'gif -index {i}').subsample(scale_factor)
            for i in range(num_frames)
        ]
        self.loader_label = tk.Label(self)

    def update_frame(self, frame_number=0):
        frame = self.loader_frames[frame_number]
        self.loader_label.configure(image=frame)
        next_frame = (frame_number + 1) % len(self.loader_frames)
        self.after(100, self.update_frame, next_frame)  # Adjust time for frame change

    def show_loader(self):
        self.loader_label.grid(row=1, column=0, pady=10)
        self.update_frame()

    def hide_loader(self):
        self.loader_label.grid_remove()
        tk.Label(self, text="Download complete.").grid(row=1, column=0)

    def process_photos(self, timestamp):
        photos = self.extensions['apple'].apple_login.photos.albums['All Photos']

        for photo in photos:
            newDate = adjust_apple_time(photo.created)
            if newDate.date() >= timestamp:
                self.process_photo(photo, newDate)
            else:
                break

        self.hide_loader()

    def on_close(self, cal, top):
        timestamp = cal.selection_get()
        top.destroy()

        # Hide calendar button
        self.calendar_button.grid_remove()
        self.show_loader()

        # Start the download process in a separate thread
        threading.Thread(target=self.process_photos, args=(timestamp,), daemon=True).start()

    def process_photo(self, photo, new_date):
        """
        Process and download a photo from iCloud.

        Parameters:
        photo (obj): The photo object to download.
        new_date (datetime): The date for naming the downloaded file.
        """
        date_string = f"{new_date.year}-{new_date.month}-{new_date.day}"

        if not os.path.exists(date_string):
            os.makedirs(date_string)

        extension = photo.versions['original']['filename'].split(".")[1]
        filename = f"{date_string}/{new_date.month}-{new_date.day}-{new_date.year}-{new_date.hour}-{new_date.minute}-{new_date.second}-{new_date.microsecond}.{extension}"

        if "heic" in photo.filename.lower():
            download = photo.download('medium')
            video_name = filename.replace('.HEIC', '.mov')
            with open(video_name, 'wb') as file:
                file.write(download.raw.read())
            self.extract_first_frame(video_name)
        else:
            download = photo.download('original')
            with open(filename, 'wb') as file:
                file.write(download.raw.read())

    def create_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Input Required")
        popup.geometry("300x100")

        tk.Label(popup, text="Enter your value:").pack(pady=5)

        input_value = tk.StringVar()
        input_field = tk.Entry(popup, textvariable=input_value)
        input_field.pack(pady=5)

        def on_submit():
            popup.destroy()

        submit_button = tk.Button(popup, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

        # Focus on the input field and wait for the popup to close
        input_field.focus_set()
        popup.grab_set()
        popup.wait_window()

        return input_value.get()

    def extract_first_frame(self, video_path):
        """
        Extract the first frame from a video file and save it as an image.

        Parameters:
        video_path (str): The path of the video file.

        """
        directory, filename = os.path.split(video_path)
        name, _ = os.path.splitext(filename)
        capture = cv2.VideoCapture(video_path)
        success, image = capture.read()
        if success:
            cv2.imwrite(os.path.join(directory, f"{name}.jpg"), image)

    def login_to_icloud(self):

        username = self.username_input.get()
        password = self.password_input.get()

        ICB.init_app(app, username, password)

        # Hide login frame
        self.login_frame.grid_remove()

        # Show calendar button
        self.calendar_button.grid(row=0, column=0, pady=10)

    def show_date_picker(self):
        top = tk.Toplevel(self)
        cal = Calendar(top, selectmode='day')
        cal.pack(pady=20)

        def handle_close():
            self.calendar_button.grid_remove()  # Hide calendar button
            self.on_close(cal, top)

        tk.Button(top, text="OK", command=handle_close).pack()


if __name__ == "__main__":
    app = iCloudPhotoGrabber()
    sv_ttk.set_theme("light")
    app.mainloop()
