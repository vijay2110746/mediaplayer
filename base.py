from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
import os

class VideoPlayerApp(App):
    def build(self):
        self.volume = 100 
        self.video_player = VideoPlayer()
        self.video_player.state = 'play'
        self.current_index = 0
        self.sound=None
        self.image = Image(size_hint=(1, 0.9))
        self.image.allow_stretch = True
        self.image.keep_ratio = True

        button_height = 40
        button_background_color = (0.2, 0.6, 0.8, 1)
        padding = 10
        spacing=20


        self.image1 = Image(source=r"C:\Users\vijay\OneDrive - SSN Trust\Desktop\sem 5\meister gen\icon.png", size_hint=(1, 0.3))

        self.progress_slider = Slider(min=0, max=100, value=0, size_hint=(1, None), height=50)

        self.browse_button = Button(text='Browse', size_hint=(None, None), size=(120, button_height), background_color=button_background_color)
        self.browse_button.bind(on_press=self.browse_files)

        self.play_button = Button(text='Play', size_hint=(None, None), size=(120, button_height), background_color=button_background_color)
        self.play_button.bind(on_press=self.toggle_play)
    
        self.volume_slider = Slider(min=0, max=1, value=self.volume, orientation='horizontal', size_hint=(1, None), height=50)
        self.volume_slider.bind(value=self.on_volume_changed)

        self.next_button = Button(text='Next', size_hint=(None, None), size=(120, button_height), background_color=button_background_color)
        self.next_button.bind(on_press=self.play_next_video)
        
        self.prev_button = Button(text='Previous', size_hint=(None, None), size=(120, button_height), background_color=button_background_color)
        self.prev_button.bind(on_press=self.play_previous_video)

        self.browse_button1 = Button(text='Browse', size_hint=(None, None), size=(120, button_height), background_color=button_background_color)
        self.browse_button1.bind(on_press=self.browse_files)


        self.volume_slider1 = Slider(min=0, max=1, value=self.volume, orientation='horizontal', size_hint=(1, None), height=50)
        self.volume_slider.bind(value=self.on_volume_changed1)
        self.next_button1 = Button(text='Next', size_hint=(None, None), size=(120, button_height), background_color=button_background_color)
        self.next_button1.bind(on_press=self.play_next_video)
        
        self.prev_button1 = Button(text='Previous', size_hint=(None, None), size=(120, button_height), background_color=button_background_color)
        self.prev_button1.bind(on_press=self.play_previous_video)


        self.buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=button_height, padding=padding, spacing=20)
        self.buttons_layout.add_widget(self.prev_button)
        self.buttons_layout.add_widget(self.browse_button)
        self.buttons_layout.add_widget(self.next_button)
        self.buttons_layout.add_widget(self.volume_slider)

        self.buttons_layout1 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, padding=20, spacing=20)
        self.buttons_layout1.add_widget(self.play_button)
        self.buttons_layout1.add_widget(self.next_button1)
        self.buttons_layout1.add_widget(self.prev_button1)
        self.buttons_layout1.add_widget(self.browse_button1)
        self.buttons_layout1.add_widget(self.volume_slider1)

        self.buttons_layout2 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=button_height, padding=padding, spacing=20)
        self.browse_button2 = Button(text='Browse', size_hint=(None, None), size=(100, button_height), background_color=button_background_color)
        self.browse_button2.bind(on_press=self.browse_files)
        self.next_button2 = Button(text='Next', size_hint=(None, None), size=(100, button_height), background_color=button_background_color)
        self.next_button2.bind(on_press=self.play_next_video)
        self.prev_button2 = Button(text='Previous', size_hint=(None, None), size=(100, button_height), background_color=button_background_color)
        self.prev_button2.bind(on_press=self.play_previous_video)

        self.buttons_layout2.add_widget(self.prev_button2)
        self.buttons_layout2.add_widget(self.browse_button2)
        self.buttons_layout2.add_widget(self.next_button2)

        self.main_layout = BoxLayout(orientation='vertical',spacing=spacing)
        self.main_layout.add_widget(self.video_player)
        self.main_layout.add_widget(self.buttons_layout)



        return self.main_layout

    def toggle_play(self, instance):
        if self.playing:
            self.sound.stop()
            self.play_button.text = 'Play'
        else:
            self.sound.play()
            self.play_button.text = 'Pause'
        self.playing = not self.playing

    def update_progress(self, dt):
        if self.sound:
            self.progress_slider.value = self.sound.get_pos()

    def seek_to(self, instance, value):
        if self.sound:
            self.sound.seek(value)

    def seek_forward(self, instance):
        if self.video_player.state == 'play':
            self.video_player.seek(self.video_player.position+10)

    def seek_backward(self, instance):
        if self.video_player.state == 'play':
            self.video_player.seek(self.video_player.position-10)

    def browse_files(self, instance):

        file_chooser = self.create_file_chooser()
        file_chooser.bind(on_submit=self.load_video)
        self.popup = Popup(title='Select Video File', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def create_file_chooser(self):

        file_chooser = FileChooserListView()
        file_chooser.path = os.path.expanduser('~') 
        # print(file_chooser) 
        return file_chooser

    def load_video(self, instance, selection, touch):
        if selection:


            selected_file = selection[0]
            print(selected_file)
            self.popup.dismiss()
            f=selected_file
            r = ''
            l = []
            f = f.split('\\')
            f = f[:len(f) - 1]
            folder_path = ''
            for i in f:
                if i != f[-1]:
                    folder_path += i + "\\"
                else:
                    folder_path += i
            
            print('folder',folder_path)
            if folder_path:
                self.media_files = self.get_supported_media_files(folder_path)
                for i in range(len(self.media_files)):
                    if self.media_files[i] == selected_file:
                        ind = i
                if self.media_files:
                    self.current_index = ind
                    self.play_next_video()
            


    def play_next_video(self, instance=None):
        if self.media_files:
            if self.current_index < len(self.media_files):
                file_url = self.media_files[self.current_index]
                if file_url.endswith('.mp3') or file_url.endswith('.wav'):
                    if self.sound:
                        self.sound.stop()
                    self.video_player.state='pause'
                    self.sound = SoundLoader.load(file_url)
                    self.main_layout.remove_widget(self.image1)
                    self.main_layout.remove_widget(self.progress_slider)
                    self.main_layout.remove_widget(self.image)
                    self.main_layout.remove_widget(self.buttons_layout2)
                    self.main_layout.remove_widget(self.buttons_layout1)
                    self.main_layout.remove_widget(self.video_player)
                    self.main_layout.remove_widget(self.buttons_layout)
                    self.main_layout.add_widget(self.image1)
                    self.main_layout.add_widget(self.progress_slider)
                    
                    self.main_layout.add_widget(self.buttons_layout1)
                    if self.sound:
                        self.sound.play()
                        self.play_button.text = 'Pause'
                        self.progress_slider.max = self.sound.length
                        Clock.schedule_interval(self.update_progress, 1)
                elif file_url.endswith('.mp4') or file_url.endswith('.avi') or file_url.endswith('mkv'):                # 'avi', 'wmv', 'mov', 'mkv', 'flv'
                    if self.sound:
                        self.sound.stop()
                    self.main_layout.remove_widget(self.image1)
                    self.main_layout.remove_widget(self.buttons_layout1)
                    self.main_layout.remove_widget(self.image)
                    self.main_layout.remove_widget(self.buttons_layout2)
                    self.main_layout.remove_widget(self.video_player)
                    self.main_layout.remove_widget(self.buttons_layout)
                    self.main_layout.remove_widget(self.progress_slider)
                    self.main_layout.add_widget(self.video_player)
                    self.main_layout.add_widget(self.buttons_layout)
                    self.video_player.state='play'
                    self.video_player.source = file_url
                else:
                    if self.sound:
                        self.sound.stop()
                    self.video_player.state='pause'
                    self.image.source=file_url
                    self.main_layout.remove_widget(self.image1)
                    self.main_layout.remove_widget(self.progress_slider)
                    self.main_layout.remove_widget(self.image)
                    self.main_layout.remove_widget(self.buttons_layout2)
                    self.main_layout.remove_widget(self.buttons_layout1)
                    self.main_layout.remove_widget(self.video_player)
                    self.main_layout.remove_widget(self.buttons_layout)
                    self.main_layout.add_widget(self.image)
                    self.main_layout.add_widget(self.buttons_layout2)

                self.current_index += 1
                if self.current_index >= len(self.media_files):
                    self.current_index = 0



    def play_previous_video(self, instance):
        if self.media_files:
            self.current_index -= 2
            if self.current_index < 0:
                self.current_index = len(self.media_files) - 1
            self.play_next_video()

    def on_volume_changed1(self, instance, value):
        self.volume = value
        if self.sound:
            self.sound.volume = value / 100

    def on_volume_changed(self, instance, value):
        self.volume = value

        self.video_player.volume = value

    def get_supported_media_files(self, folder_path):
        supported_formats = {'mp4', 'avi', 'wmv', 'mov', 'mkv', 'flv','mp3','wav','jpg','png','jpeg'}
        media_files = []
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                file_extension = os.path.splitext(filename)[1][1:].lower()
                if file_extension in supported_formats:
                    media_files.append(filepath)
        print(media_files)
        return media_files


if __name__ == '__main__':
    VideoPlayerApp().run()


