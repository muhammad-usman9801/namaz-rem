import time
from tkinter.tix import PopupMenu
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.clock import Clock
from plyer import notification
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class CustomPopupMenu(Popup):
    def __init__(self, **kwargs):
        super(CustomPopupMenu, self).__init__(**kwargs)

        # Create a BoxLayout as the content of the popup
        content_layout = BoxLayout(orientation='vertical', spacing=5)

        # Add your custom widgets here
        option1_button = Button(text='Option 1', size_hint_y=None, height=40)
        option2_button = Button(text='Option 2', size_hint_y=None, height=40)
        separator_label = Label(text='----------------------', size_hint_y=None, height=10)
        about_button = Button(text='About', size_hint_y=None, height=40)

        # Add the buttons or other widgets to the content layout
        content_layout.add_widget(option1_button)
        content_layout.add_widget(option2_button)
        content_layout.add_widget(separator_label)
        content_layout.add_widget(about_button)

        # Set the content of the popup to the custom layout
        self.content = content_layout

        # Customize the popup appearance and behavior
        self.size_hint = (None, None)
        self.size = (200, 200)

        # Add your additional customizations here, such as bindings or callbacks
        about_button.bind(on_press=self.show_about_popup)


class PrayerTimeApp(App):
    def build(self):
        self.icon = 'background.png'  # Set the app icon

        self.screen_manager = ScreenManager(transition=SlideTransition())

        self.start_screen = Screen(name='start')
        start_layout = BoxLayout(orientation='vertical', spacing=10)
        start_layout.add_widget(Image(source='starting.jpg', allow_stretch=True, keep_ratio=True, opacity=0))

        self.start_screen.add_widget(start_layout)

        self.main_screen = Screen(name='main')
        main_layout = BoxLayout(orientation='vertical', spacing=10)
        top_bar_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        # Three-dot button to open the menu
        menu_button = Button(text='Menu', size_hint=(None, 1), font_size='24sp')
        menu_button.bind(on_press=self.open_menu)
        top_bar_layout.add_widget(menu_button)

        main_layout.add_widget(top_bar_layout)

        # Set the background image
        main_layout.add_widget(Image(source='background.png', allow_stretch=True))

        main_layout.add_widget(Label(text='Prayer Time App', font_size='35sp', color=(0, 0.7, 1, 1)))

        self.mode_button = ToggleButton(text='Set Silent Mode', on_press=self.toggle_mode, font_size='18sp')
        main_layout.add_widget(self.mode_button)

        self.prayer_label = Label(text='Current Prayer: -', font_size='20sp')
        main_layout.add_widget(self.prayer_label)

        self.timer_label = Label(text='Time until next prayer: -', font_size='20sp')
        main_layout.add_widget(self.timer_label)

        self.refresh_button = Button(text='Refresh Prayer Times', on_press=self.refresh_prayer_times, font_size='22sp')
        main_layout.add_widget(self.refresh_button)

        self.main_screen.add_widget(main_layout)

        self.config_screen = Screen(name='config')
        config_layout = BoxLayout(orientation='vertical', spacing=10)
        config_layout.add_widget(Label(text='Set Custom Prayer Times', font_size='25sp', color=(1, 0.5, 0, 1)))

        self.custom_prayer_inputs = {}
        for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
            input_label = Label(text=f'{prayer} Time:', font_size='20sp')
            input_text = TextInput(font_size='20sp')
            config_layout.add_widget(input_label)
            config_layout.add_widget(input_text)
            self.custom_prayer_inputs[prayer] = input_text

        config_layout.add_widget(Button(text='Save Custom Times', on_press=self.save_custom_prayer_times, font_size='20sp'))
        self.config_screen.add_widget(config_layout)

        self.screen_manager.add_widget(self.start_screen)
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.config_screen)

        # Start with the starting screen
        Clock.schedule_once(self.fade_in_start_screen, 0)

        self.settings = {
            'location': 'City, Country',
            'notification': True,
            'countdown': True
        }

        self.prayer_times = self.fetch_prayer_times()
        self.current_prayer_index = 0
        self.update_prayer_label()
        self.update_timer_label()

        Clock.schedule_interval(self.check_prayer_time, 60)  # Check every minute

        return self.screen_manager

    def fade_in_start_screen(self, dt):
        # Animate the fade-in effect for the starting screen
        start_layout = self.start_screen.children[0]
        start_layout.children[0].opacity = 1  # Set opacity to 1 for a fade-in effect
        Clock.schedule_once(lambda dt: self.switch_to_main_screen(None), 4)  # Switch to the main screen after 4 seconds

    def switch_to_start_screen(self, dt):
        self.screen_manager.current = 'start'

    def switch_to_main_screen(self, instance):
        self.screen_manager.current = 'main'

    def switch_to_config_screen(self, instance):
        self.screen_manager.current = 'config'

    def toggle_mode(self, instance):
        if instance.state == 'down':
            self.set_silent_mode()
        else:
            self.set_normal_mode()

    def set_silent_mode(self):
        try:
            # Implement the code to change the phone mode here
            # For demonstration purposes, print a message
            print('Silent mode activated.')
            self.show_notification('Silent mode activated.')

            # Schedule the timer to switch back to normal mode after 15 minutes
            Clock.schedule_once(lambda dt: self.set_normal_mode(), 900)  # 900 seconds = 15 minutes
        except Exception as e:
            print(f'Error: {e}')
            self.show_notification('Error occurred while setting silent mode.')

    def set_normal_mode(self):
        # Implement the code to change the phone mode here
        # For demonstration purposes, print a message
        print('Normal mode activated.')
        self.show_notification('Normal mode activated.')

    def open_menu(self, instance):
        menu = BoxLayout(orientation='vertical', padding=10, spacing=5)
        menu.add_widget(Button(text='Help', on_press=self.show_help))
        menu.add_widget(Button(text='About', on_press=self.show_about))
        menu.add_widget(Button(text='Settings', on_press=self.open_settings))

        popup = Popup(title='Menu', content=menu, size_hint=(None, None), size=(150, 150))

        popup.open()

    def show_help(self, instance):
        help_text = (
            "Help:\n"
            "This app helps you manage prayer times and phone modes.\n"
            "Silent mode will be activated during prayer times."
        )
        self.show_info_popup('Help', help_text)

    def show_about(self, instance):
        about_text = (
            "About:\n"
            "Developer: Muhammad Usman Rouf\n"
            "Team CEO: Muhammad Usman\n"
            "Company: STRANGER(AI) Group Co\n\n"
            "Copyright © 2023 STRANGER(AI) Group."
        )
        self.show_info_popup('About', about_text)

    def open_settings(self, instance):
        self.switch_to_config_screen(None)

    def update_settings(self, instance):
        self.settings = instance.json_data
        self.prayer_times = self.fetch_prayer_times()  # Refresh prayer times after settings change
        self.update_prayer_label()
        self.update_timer_label()

    def build_config(self, config):
        config.setdefaults('app', {'location': 'City, Country', 'notification': True, 'countdown': True})

    def on_config_change(self, config, section, key, value):
        if section == 'app' and key == 'location':
            self.prayer_times = self.fetch_prayer_times()
            self.update_prayer_label()
            self.update_timer_label()

    def show_notification(self, message):
        if self.settings['notification']:
            notification.notify(
                title='Prayer Time App',
                message=message,
                app_name='Prayer Time App'
            )

    def show_info_popup(self, title, text):
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        content.add_widget(Label(text=text, size_hint_y=None, height=100))

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def fetch_prayer_times(self):
        # For demonstration purposes, return fixed prayer times in 24-hour format
        return {
            'Fajr': '5:30',
            'Dhuhr': '12:30',
            'Asr': '16:00',
            'Maghrib': '18:45',
            'Isha': '20:30'
        }

    def refresh_prayer_times(self, instance):
        self.prayer_times = self.fetch_prayer_times()
        self.update_prayer_label()
        self.update_timer_label()
        self.show_notification('Prayer times refreshed.')

    def save_custom_prayer_times(self, instance):
        custom_prayer_times = {}
        for prayer, input_text in self.custom_prayer_inputs.items():
            custom_time = input_text.text.strip()
            if custom_time:
                custom_prayer_times[prayer] = custom_time
            else:
                # If any custom time is empty, use the default time
                return self.fetch_prayer_times()

        self.prayer_times = custom_prayer_times
        self.switch_to_main_screen(None)
        self.update_prayer_label()
        self.update_timer_label()

    def schedule_notifications(self):
        for prayer, time in self.prayer_times.items():
            # Schedule notification for each prayer time
            self.schedule_notification(prayer, time)

    def schedule_notification(self, prayer, time):
        # Convert prayer time to seconds since midnight
        prayer_time_seconds = sum(x * int(t) for x, t in zip([3600, 60], time.split(':')))

        # Calculate time until prayer in seconds
        current_time = time.localtime()
        current_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60 + current_time.tm_sec
        time_until_prayer = prayer_time_seconds - current_seconds

        # Schedule notification
        if time_until_prayer > 0:
            Clock.schedule_once(lambda dt: self.show_notification(f"{prayer} prayer time at {time}"), time_until_prayer)

    def check_prayer_time(self, dt):
        # Check if it's time for the next prayer
        current_time_struct = time.localtime()
        current_seconds = current_time_struct.tm_hour * 3600 + current_time_struct.tm_min * 60 + current_time_struct.tm_sec

        next_prayer_index = (self.current_prayer_index + 1) % len(self.prayer_times)
        next_prayer_time = list(self.prayer_times.values())[next_prayer_index]
        next_prayer_seconds = sum(x * int(t) for x, t in zip([3600, 60], next_prayer_time.split(':')))

        time_until_next_prayer = next_prayer_seconds - current_seconds
        if time_until_next_prayer < 0:
            time_until_next_prayer += 24 * 3600  # Add 24 hours if the next prayer is in the past

        if self.current_prayer_index != next_prayer_index:
            self.current_prayer_index = next_prayer_index
            self.update_prayer_label()
            self.update_timer_label()

    def update_prayer_label(self):
        current_prayer = list(self.prayer_times.keys())[self.current_prayer_index]
        self.prayer_label.text = f'Current Prayer: {current_prayer}'

    def update_timer_label(self):
        if self.settings['countdown']:
            time_until_next_prayer = self.calculate_time_until_next_prayer()
            self.timer_label.text = f'Time until next prayer: {self.format_time(time_until_next_prayer)}'
        else:
            self.timer_label.text = 'Time until next prayer: -'

    def calculate_time_until_next_prayer(self):
        current_time = time.localtime()
        current_seconds = current_time.tm_hour * 3600 + current_time.tm_min * 60 + current_time.tm_sec

        next_prayer_index = (self.current_prayer_index + 1) % len(self.prayer_times)
        next_prayer_time = list(self.prayer_times.values())[next_prayer_index]
        next_prayer_seconds = sum(x * int(t) for x, t in zip([3600, 60], next_prayer_time.split(':')))

        return max(0, next_prayer_seconds - current_seconds)

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f'{int(hours)}h {int(minutes)}m'


if __name__ == '__main__':
    PrayerTimeApp().run()
