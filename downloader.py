from __consts__ import *

import os, re, traceback, time, ssl
import certifi

from kivy.logger import Logger
from kivy.config import ConfigParser

from pytube import Playlist, YouTube
import ffmpeg


class Downloader:
    def __init__(self) -> None:
        ssl._create_default_https_context = ssl._create_stdlib_context
        os.environ["SSL_CERT_FILE"] = certifi.where()

        self.downloading: bool = False

        self.config: ConfigParser = ConfigParser()
        self.config.read(INI_FILE_DIR)

    def download_video(self, video: YouTube):
        title = re.sub(REGEX_TITLE, "", video.title)

        Logger.info(LOG_TAG + "Downloading: " + title)

        output_folder: str = self.config.get(FOLDER_SECTION, OUTPUT_FOLDER_SETTING)

        if not os.path.exists(output_folder):
            try:
                os.mkdir(output_folder)
            except:
                Logger.error(DOWNLOAD_ERROR, exc_info=traceback.format_exc())

        try:
            temp_video_path: str = video.streams.get_audio_only().download(
                output_path=TEMP_FOLDER,
                filename=title + VIDEO_EXTENSION,
                max_retries=MAX_RETRIES,
            )

            temp_music_path = os.path.join(TEMP_FOLDER, title + MUSIC_EXTENSION)

            ffmpeg.input(temp_video_path).output(temp_music_path).run()

            output = os.path.join(output_folder, title + MUSIC_EXTENSION)

            os.rename(temp_music_path, output)

            Logger.info(DOWNLOAD_SUCCESS)
        except:
            Logger.error(DOWNLOAD_ERROR, exc_info=traceback.format_exc())

    def download_playlist(self, playlist: Playlist):
        for video in playlist.videos:
            self.download_video(video)
            time.sleep(PLAYLIST_SLEEP_TIME)

        Logger.info(DOWNLOAD_PLAYLIST)

    def download(self, url: str):
        self.downloading = True

        try:
            if self.is_playlist(url):
                self.download_playlist(Playlist(url))
            else:
                self.download_video(YouTube(url))
        except:
            Logger.error(URL_ERROR, exc_info=traceback.format_exc())

        self.downloading = False

    def is_playlist(self, url: str) -> bool:
        return url.find(URL_PLAYLIST_SUBSTR) != NOT_PLAYLIST
