from datetime import datetime

TITLE: str = "Youtube Audio Downloader"
LOG_FOLDER: str = "./logs/"
LOG_FILE_NAME_FORMAT: str = LOG_FOLDER + "{:%Y-%m-%d}.log".format(datetime.now())
LOG_MESSAGE_FORMAT: str = "%(asctime)s [%(levelname)s]: %(message)s"
CREATING_FOLDER_LOG: str = "Creating log folder."
LOGGER_WRITTING_LOG_FILE: str = "Writting on log file."
SAVING_LOG: str = "Saving log {0}/{1}"
LOG_SAVED: str = "Log file saved!"
LOG_TAG: str = "Program: "


LAYOUT_FILE: str = "./layout.kv"

BG_IMAGE: str = "./assets/background.jpeg"
BTN_UP_IMAGE: str = "./assets/button.jpeg"
BTN_DOWN_IMAGE: str = "./assets/button_down.jpeg"
ICO_IMAGE: str = "./assets/icon.png"
TITLE_IMAGE: str = "./assets/title.png"
URL_LABEL_IMAGE: str = "./assets/url_label.png"
LOG_BUTTON_UP_IMAGE: str = "./assets/log_button.png"
LOG_BUTTON_DOWN_IMAGE: str = "./assets/log_button_down.png"

ERROR_COLOR: tuple = (1, 0, 0, 1)
INFO_COLOR: tuple = (0, 1, 0, 1)

OUTPUT: str = "./output/"
REGEX_TITLE: str = r"([^a-zA-Z0-9\s\.\-_áéíóú])+"
FILE_EXTENSION:str = ".mp3"

URL_PLAYLIST_SUBSTR: str = "playlist?list="

PLAYLIST_SLEEP_TIME: float = 1.5

APP_ERROR: str = "Error while running app"
URL_ERROR: str = LOG_TAG + "Error getting video or playlist. Please, check URL"
DOWNLOAD_SUCCESS: str = LOG_TAG + "Download Success!"
DOWNLOAD_ERROR: str = LOG_TAG + "Error downloading music"
DOWNLOAD_PLAYLIST: str = LOG_TAG + "Playlist downloaded"
