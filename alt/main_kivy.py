from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.core.window import Window

# Optional: Set a default window size (for testing purposes)
Window.size = (360, 640)

class iCloudPhotoGrabber(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Calendar Button
        self.calendar_button = Button(
            text='Select date',
            background_color=(0.1, 0.5, 0.8, 1),  # Blue color
            background_normal='',  # Required to apply custom color
            size_hint_y=None,
            height=50,
            border=(15, 15, 15, 15)
        )
        self.calendar_button.bind(on_release=self.show_date_picker)
        self.add_widget(self.calendar_button)

        self.cal_status = Label(text='')
        self.add_widget(self.cal_status)

        # iCloud Login
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.add_widget(self.username_input)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        self.add_widget(self.password_input)

        self.login_button = Button(
            text='Login',
            background_color=(0.1, 0.7, 0.1, 1),  # Green color
            background_normal='',
            size_hint_y=None,
            height=50,
            border=(15, 15, 15, 15)
        )
        self.login_button.bind(on_press=self.login_to_icloud)
        self.add_widget(self.login_button)

        self.login_status = Label(text='')
        self.add_widget(self.login_status)

        # Download Photos Button
        self.download_button = Button(
            text='Download Photos',
            background_color=(0.8, 0.3, 0.1, 1),  # Orange color
            background_normal='',
            size_hint_y=None,
            height=50,
            border=(15, 15, 15, 15)
        )
        self.download_button.bind(on_press=self.download_photos)
        self.add_widget(self.download_button)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def login_to_icloud(self, instance):
        username = self.username_input.text
        password = self.password_input.text

    def download_photos(self, instance):
        username = self.username_input.text

class MyApp(App):
    def build(self):
        return iCloudPhotoGrabber()

if __name__ == '__main__':
    MyApp().run()
