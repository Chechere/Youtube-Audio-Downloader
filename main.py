from varfile import *

import os, re, ssl, time, traceback
from threading import Thread

from kivy.app import App, ObjectProperty
from kivy.lang import Builder
#from kivy.utils import platform
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from pytube import Playlist, YouTube

from android.permissions import Permission, request_permissions

import certifi

class AppGrid(Widget):
    info_label: Label = ObjectProperty(None)
    text_input: TextInput = ObjectProperty(None)
    download_button: Button = ObjectProperty(None)
    
    background_app: Image

    def __init__(self, **kwargs):
        self.background_app = Image(source=BG_IMAGE).texture
        self.background_app.wrap = "repeat"
        self.background_app.uvsize = (8, -1)

        super().__init__(**kwargs)

    def show_info(self, info: str, color = INFO_COLOR):
        self.info_label.color = color
        self.info_label.text = info

    def download_video(self, video):
        title = re.sub(REGEX_TITLE, "", video.title) + FILE_EXTENSION

        self.show_info('Downloading: ' + title)

        try:
            video.streams.get_audio_only().download(output_path=OUTPUT, filename=title, max_retries=3)
            self.show_info(DOWNLOAD_SUCCESS)
        except Exception:
            self.show_info(DOWNLOAD_ERROR, ERROR_COLOR)

    def download_playlist(self, playlist):
        for video in playlist.videos:
            self.download_video(video)
            time.sleep(PLAYLIST_SLEEP_TIME)

        self.show_info(DOWNLOAD_PLAYLIST)

    def download(self, url):
        self.info_label.text = "patata"

        try:
            if self.isPlaylist(url):
                self.download_playlist(Playlist(url))
            else:
                self.download_video(YouTube(url))
        except BaseException:
            self.show_info(URL_ERROR, ERROR_COLOR)
            with open(OUTPUT + "/error.txt", "w") as f:
                f.write(traceback.format_exc())

        self.download_button.disabled = False

    def isPlaylist(self, url: str) -> bool:
        return url.find(URL_PLAYLIST_SUBSTR) != -1

    def button_click(self, instance):
        self.download_button.disabled = True
        Thread(target=self.download, args=[self.text_input.text]).start()

class PytubeApp(App):
    def build(self):
        self.root = Builder.load_file(LAYOUT_FILE)

        return AppGrid()

if __name__ == '__main__':
    request_permissions(
        [
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.INTERNET,
            Permission.ACCESS_NETWORK_STATE,
            Permission.ACCESS_WIFI_STATE,
        ]
    )
    
    ssl._create_default_https_context = ssl._create_stdlib_context
    os.environ['SSL_CERT_FILE'] = certifi.where()

    PytubeApp().run()
