from __consts__ import *

import os, traceback, logging, shutil

from logging import LogRecord
from threading import Thread

from kivy.app import App, ObjectProperty
from kivy.config import Config, ConfigParser
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.settings import Settings
from kivy.logger import Logger, LoggerHistory
from kivy.utils import platform

if platform == ANDROID_PLATFORM:
    from android.permissions import Permission, request_permissions  # type: ignore
    from android.storage import primary_external_storage_path, app_storage_path  # type: ignore

from downloader import Downloader


class LogLabelHander(logging.Handler):
    def __init__(self, label):
        super(LogLabelHander, self).__init__()
        self.label = label

    def emit(self, record):
        if not LOG_TAG in record.getMessage():
            return

        if record.levelno == logging.ERROR:
            self.label.color = ERROR_COLOR
        elif record.levelno == logging.INFO:
            self.label.color = INFO_COLOR
        else:
            self.label.color = (1, 1, 1, 1)

        self.label.text = record.getMessage().removeprefix(LOG_TAG)


class AppGrid(Widget):
    info_label: Label = ObjectProperty(None)
    text_input: TextInput = ObjectProperty(None)
    download_button: Button = ObjectProperty(None)

    background_app: Image

    def __init__(self, **kwargs):
        self.background_app: Image = Image(source=BG_IMAGE).texture

        self.downloader: Downloader = Downloader()

        self.config: ConfigParser = ConfigParser()
        self.config.read(INI_FILE_DIR)

        super().__init__(**kwargs)

        Logger.addHandler(LogLabelHander(self.info_label))

    def button_click(self, instance):
        if self.downloader.downloading:
            return

        Thread(target=self.downloader.download, args=[self.text_input.text]).start()

    def save_log_click(self, instance):
        log_folder: str = self.config.get(FOLDER_SECTION, LOG_FOLDER_SETTING)

        if not os.path.isdir(log_folder):
            Logger.info(CREATING_FOLDER_LOG)
            try:
                os.makedirs(log_folder)
            except:
                Logger.error(CREATE_LOG_FOLDER_ERROR, exc_info=traceback.format_exc())
                log_folder = DEFAULT_LOG_FOLDER

        try:
            fh = logging.FileHandler(os.path.join(TEMP_FOLDER, LOG_FILE_NAME_FORMAT))
            fh.setFormatter(logging.Formatter(LOG_MESSAGE_FORMAT))
            fh.setLevel(logging.DEBUG)

            Logger.info(LOGGER_WRITTING_LOG_FILE)

            log: LogRecord
            for log in reversed(LoggerHistory.history):
                fh.emit(log)

            Logger.info(LOG_SAVED)
            fh.emit(LoggerHistory.history[0])
            fh.close()

            shutil.move(
                os.path.join(TEMP_FOLDER, LOG_FILE_NAME_FORMAT),
                os.path.join(log_folder, LOG_FILE_NAME_FORMAT),
            )
        except:
            Logger.error(CREATE_LOG_FILE_ERROR, exc_info=traceback.format_exc())


class YTAudioDownloader(App):
    def build(self):
        self.title = TITLE
        self.icon = ICO_IMAGE
        self.root = Builder.load_file(LAYOUTS_FILE)
        self.use_kivy_settings = False

        return AppGrid()

    def on_start(self):
        if platform == ANDROID_PLATFORM:
            request_permissions(
                [
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.INTERNET,
                    Permission.ACCESS_NETWORK_STATE,
                    Permission.ACCESS_WIFI_STATE,
                ]
            )

    def build_settings(self, settings: Settings):
        config: ConfigParser = ConfigParser()
        config.read(INI_FILE_DIR)

        settings.add_json_panel(title=TITLE, config=config, data=JSON_FILE)

        return super().build_settings(settings)


def create_ini_file():
    with open(INI_FILE_DIR, "w") as f:
        f.writelines([string + "\n" for string in INI_DEFAULT_FILE])


if __name__ == "__main__":
    if not os.path.isfile(INI_FILE_DIR):
        create_ini_file()

    try:
        Config.set("graphics", "resizable", False)

        app: YTAudioDownloader = YTAudioDownloader()
        app.run()
    except BaseException:
        print("ERROR! ", APP_ERROR)
        print(traceback.format_exc())

        fh = logging.FileHandler(LOG_FILE_NAME_FORMAT)
        fh.setFormatter(logging.Formatter(LOG_MESSAGE_FORMAT))
        fh.setLevel(logging.DEBUG)

        fh.emit(
            LogRecord(
                level=logging.ERROR,
                name=APP_ERROR,
                msg=traceback.format_exc(),
                exc_info=None,
                pathname=None,
                args=None,
                lineno=None,
            )
        )
