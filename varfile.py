import os
#from kivy.utils import platform
from android.storage import primary_external_storage_path



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

OUTPUT: str = "./"
OUTPUT: str = os.path.join(primary_external_storage_path(), 'Download')
REGEX_TITLE: str = r"([^a-zA-Z0-9\s\.\-_áéíóú])+"
FILE_EXTENSION: str = ".mp3"

URL_PLAYLIST_SUBSTR: str = "playlist?list="

PLAYLIST_SLEEP_TIME: float = 1.5

APP_ERROR: str = "Error while running app"
URL_ERROR: str = "Error getting video or playlist. Please, check URL"
DOWNLOAD_SUCCESS: str = "Download Success!"
DOWNLOAD_ERROR: str = "Error downloading music"
DOWNLOAD_PLAYLIST: str = "Playlist downloaded"
