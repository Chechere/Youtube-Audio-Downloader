from datetime import datetime
from pathlib import Path
import os

TITLE: str = "Youtube Audio Downloader"

#INI DATA
INI_FILE_DIR = "./config.ini"
DEFAULT_LOG_FOLDER: str = str(Path.cwd() / "logs")
DEFAULT_OUTPUT_FOLDER: str = str(Path.home() / "Downloads")
OUTPUT: str = str(Path.home() / "Downloads")

#LOGS MSGS
LOG_TAG: str = "Program: "
CREATING_FOLDER_LOG: str = "Creating log folder."
LOGGER_WRITTING_LOG_FILE: str = "Writting on log file."
LOG_SAVED: str = "Log file saved!"
APP_ERROR: str = "Error while running app"
URL_ERROR: str = LOG_TAG + "Error getting video or playlist. Please, check URL"
DOWNLOAD_SUCCESS: str = LOG_TAG + "Download Success!"
DOWNLOAD_ERROR: str = LOG_TAG + "Error downloading music"
DOWNLOAD_PLAYLIST: str = LOG_TAG + "Playlist downloaded"

#LOG FILE FORMAT
LOG_FILE_NAME_FORMAT: str = DEFAULT_LOG_FOLDER + "{:%Y-%m-%d}.log".format(datetime.now())
LOG_MESSAGE_FORMAT: str = "%(asctime)s [%(levelname)s]: %(message)s"

#LOG COLORS
ERROR_COLOR: tuple = (1, 0, 0, 1)
INFO_COLOR: tuple = (0, 1, 0, 1)

#ASSETS
LAYOUTS_FILE: str = "./layouts.kv"
BG_IMAGE: str = "./assets/background.jpeg"
BTN_UP_IMAGE: str = "./assets/button.jpeg"
BTN_DOWN_IMAGE: str = "./assets/button_down.jpeg"
ICO_IMAGE: str = "./assets/icon.png"
TITLE_IMAGE: str = "./assets/title.png"
URL_LABEL_IMAGE: str = "./assets/url_label.png"
LOG_BUTTON_UP_IMAGE: str = "./assets/log_button.png"
LOG_BUTTON_DOWN_IMAGE: str = "./assets/log_button_down.png"

#MUSIC FILE DATA
REGEX_TITLE: str = r"([^a-zA-Z0-9\s\.\-_áéíóú])+"
FILE_EXTENSION:str = ".mp3"

#PLAYLIST
URL_PLAYLIST_SUBSTR: str = "playlist?list="
PLAYLIST_SLEEP_TIME: float = 1.5

