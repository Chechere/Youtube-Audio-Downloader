from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp
import os

from kivy.utils import platform

TITLE: str = "Youtube Audio Downloader"
VERSION: str = "1.2.0"

ANDROID_PLATFORM: str = "android"

if platform == ANDROID_PLATFORM:
    from android.storage import primary_external_storage_path, app_storage_path  # type: ignore

    BG_IMAGE: str = "./assets/Android/background.jpeg"

    TEMP_FOLDER: str = mkdtemp(prefix="yt_audio_downloader")
    # TEMP_FOLDER: str = app_storage_path

    DEFAULT_LOG_FOLDER: str = os.path.join(
        primary_external_storage_path(), "Documents"
    )
    DEFAULT_OUTPUT_FOLDER: str = os.path.join(
        primary_external_storage_path(), "Download"
    )
else:
    BG_IMAGE: str = "./assets/PC/background.jpeg"

    TEMP_FOLDER: str = mkdtemp(prefix="yt_audio_downloader")

    DEFAULT_LOG_FOLDER: str = str(Path.cwd() / "logs")
    DEFAULT_OUTPUT_FOLDER: str = str(Path.home() / "Downloads")

# INI DATA
INI_FILE_DIR = "./config.ini"
FOLDER_SECTION = "FOLDERS"
LOG_FOLDER_SETTING = "LOG_FOLDER"
OUTPUT_FOLDER_SETTING = "OUTPUT_FOLDER"
INI_DEFAULT_FILE: list[str] = [
    "[{0}]".format(FOLDER_SECTION),
    "{0} = {1}".format(LOG_FOLDER_SETTING, DEFAULT_LOG_FOLDER),
    "{0} = {1}".format(OUTPUT_FOLDER_SETTING, DEFAULT_OUTPUT_FOLDER),
]
JSON_FILE: str = (
    """
[
    {{
        \"type\": \"title\",
        \"title\": \"Folders\"
    }},
    {{
        \"type\": \"path\",
        \"title\": \"Output Folder\",
        \"desc\": \"Set where musics should be saved\",
        \"section\": \"{0}\",
        \"key\": \"{1}\"
    }},
    {{
        \"type\": \"path\",
        \"title\": \"Log Folder\",
        \"desc\": \"Set where logs should be saved\",
        \"section\": \"{2}\",
        \"key\": \"{3}\"
    }}
]
""".format(
        FOLDER_SECTION,
        OUTPUT_FOLDER_SETTING,
        FOLDER_SECTION,
        LOG_FOLDER_SETTING,
    )
)

# LOGS MESSAGES
LOG_TAG: str = "Program: "
APP_ERROR: str = "Error while running app"
CREATING_FOLDER_LOG: str = LOG_TAG + "Creating log folder."
LOGGER_WRITTING_LOG_FILE: str = LOG_TAG + "Writting on log file."
LOG_SAVED: str = LOG_TAG + "Log file saved!"
URL_ERROR: str = LOG_TAG + "Error getting video or playlist. Please, check URL"
CREATE_OUTPUT_FOLDER_ERROR = LOG_TAG + "Error while creating output folder"
CREATE_LOG_FOLDER_ERROR = (
    LOG_TAG
    + "Error while creating log folder. Using folder: "
    + DEFAULT_LOG_FOLDER
)
CREATE_LOG_FILE_ERROR = LOG_TAG + "Error while creating log file"
DOWNLOAD_SUCCESS: str = LOG_TAG + "Download Success!"
DOWNLOAD_ERROR: str = LOG_TAG + "Error downloading music"
DOWNLOAD_PLAYLIST: str = LOG_TAG + "Playlist downloaded"
TEMP_SAVED: str = "Audio saved temporarily on: "

# LOG FILE FORMAT
LOG_FILE_NAME_FORMAT: str = "{:%Y-%m-%d}.log".format(datetime.now())
LOG_MESSAGE_FORMAT: str = "%(asctime)s [%(levelname)s]: %(message)s"

# LOG COLORS
ERROR_COLOR: tuple = (1, 0, 0, 1)
INFO_COLOR: tuple = (0, 1, 0, 1)

# ASSETS
LAYOUTS_FILE: str = "./layouts.kv"
BG_IMAGE: str = "./assets/PC/background.jpeg"
BTN_UP_IMAGE: str = "./assets/button.jpeg"
BTN_DOWN_IMAGE: str = "./assets/button_down.jpeg"
ICO_IMAGE: str = "./assets/icon.png"
TITLE_IMAGE: str = "./assets/title.png"
URL_LABEL_IMAGE: str = "./assets/url_label.png"
LOG_BUTTON_UP_IMAGE: str = "./assets/log_button.png"
LOG_BUTTON_DOWN_IMAGE: str = "./assets/log_button_down.png"

# DOWNLOADING
REGEX_RESERVED_CHARS: str = r"([^a-zA-Z0-9\s\.\-_áéíóú])+"
VIDEO_EXTENSION: str = ".mp4"
MUSIC_EXTENSION: str = ".mp3"
MAX_RETRIES: int = 3

# PLAYLIST
URL_PLAYLIST_SUBSTR: str = "playlist?list="
PLAYLIST_SLEEP_TIME: float = 1.5
NOT_PLAYLIST: int = -1
