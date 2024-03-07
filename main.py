from varfile import *

import os, re, ssl, time, logging, traceback
from threading import Thread

from kivy.app import App, ObjectProperty
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from pytube import Playlist, YouTube
import certifi

logger: logging.Logger

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

    def show_info(self, info: str, color: tuple, level: int, stacktrace: str):
        self.info_label.color = color
        self.info_label.text = info

        logger.log(level, "\n".join([info, stacktrace]))

    def show_error(self, info: str, stacktrace: str = ""):
        self.show_info(info, ERROR_COLOR, logging.ERROR, stacktrace)

    def show_debug(self, info: str, stacktrace: str = ""):
        self.show_info(info, INFO_COLOR, logging.DEBUG, stacktrace)

    def download_video(self, video):
        title = re.sub(REGEX_TITLE, "", video.title) + FILE_EXTENSION

        self.show_debug("Downloading: " + title)

        if not os.path.exists(OUTPUT):
            os.mkdir(OUTPUT)

        try:
            video.streams.get_audio_only().download(
                output_path=OUTPUT, filename=title, max_retries=3
            )
            self.show_debug(DOWNLOAD_SUCCESS)
        except BaseException:
            self.show_error(DOWNLOAD_ERROR, traceback.format_exc())

    def download_playlist(self, playlist):
        for video in playlist.videos:
            self.download_video(video)
            time.sleep(PLAYLIST_SLEEP_TIME)

        self.show_debug(DOWNLOAD_PLAYLIST)

    def download(self, url):
        self.info_label.text = ""

        try:
            if self.isPlaylist(url):
                self.download_playlist(Playlist(url))
            else:
                self.download_video(YouTube(url))
        except BaseException:
            self.show_error(URL_ERROR, traceback.format_exc())

        self.download_button.disabled = False

    def isPlaylist(self, url: str) -> bool:
        return url.find(URL_PLAYLIST_SUBSTR) != -1

    def button_click(self, instance):
        self.download_button.disabled = True
        Thread(target=self.download, args=[self.text_input.text]).start()


class YTAudioDownloader(App):
    def build(self):
        self.title = TITLE
        self.root = Builder.load_file(LAYOUT_FILE)

        return AppGrid()


def set_logger() -> logging.Logger:
    if(not os.path.isdir(LOG_FOLDER)):
        os.makedirs(LOG_FOLDER)
        
    fh = logging.FileHandler(LOG_FILE_NAME_FORMAT)
    fh.setFormatter(logging.Formatter(LOG_MESSAGE_FORMAT))
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(LOG_MESSAGE_FORMAT))
    ch.setLevel(logging.DEBUG)

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


if __name__ == "__main__":
    logger = set_logger()

    ssl._create_default_https_context = ssl._create_stdlib_context
    os.environ["SSL_CERT_FILE"] = certifi.where()

    Config.set("kivy", "window_icon", ICO_IMAGE)
    Config.set("graphics", "resizable", "0")

    try:
        YTAudioDownloader().run()
    except BaseException:
        logger.error("\n".join([APP_ERROR, traceback.format_exc()]))
