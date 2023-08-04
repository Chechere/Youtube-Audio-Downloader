from datetime import datetime

TITLE: str = "Youtube Audio Downloader"

LOG_FOLDER: str = "./logs/"
LOG_FILE_NAME_FORMAT: str = LOG_FOLDER + "{:%Y-%m-%d}.log".format(datetime.now())
LOG_MESSAGE_FORMAT: str = "%(asctime)s [%(levelname)s]: %(message)s"

LAYOUT_FILE: str = "./layout.kv"

ASSETS_FOLDER: str = "./assets/"
BG_IMAGE: str = ASSETS_FOLDER + "background.jpeg"
BTN_UP_IMAGE: str = ASSETS_FOLDER + "button.jpeg"
BTN_DOWN_IMAGE: str = ASSETS_FOLDER + "button_down.jpeg"
ICO_IMAGE: str = ASSETS_FOLDER + "icon.png"
TITLE_IMAGE: str = ASSETS_FOLDER + "title.png"
URL_LABEL_IMAGE: str = ASSETS_FOLDER + "url_label.png"

ERROR_COLOR: tuple = (1, 0, 0, 1)
INFO_COLOR: tuple = (0, 1, 0, 1)

OUTPUT: str = "./output/"
REGEX_TITLE: str = r"([^a-zA-Z0-9\s\.\-_áéíóú])+"
FILE_EXTENSION:str = ".mp3"

URL_PLAYLIST_SUBSTR: str = "playlist?list="

PLAYLIST_SLEEP_TIME: float = 1.5

APP_ERROR: str = "Error while running app"
URL_ERROR: str = "Error getting video or playlist. Please, check URL"
DOWNLOAD_SUCCESS: str = "Download Success!"
DOWNLOAD_ERROR: str = "Error downloading music"
DOWNLOAD_PLAYLIST: str = "Playlist downloaded"
