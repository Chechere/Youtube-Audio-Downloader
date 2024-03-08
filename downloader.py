from __consts__ import *

import os, re, traceback, time, ssl
import certifi

from kivy.logger import Logger

from pytube import Playlist, YouTube

class Downloader():        

    def __init__(self) -> None:
        ssl._create_default_https_context = ssl._create_stdlib_context
        os.environ["SSL_CERT_FILE"] = certifi.where()

        self.downloading: bool = False

    def download_video(self, video):
        title = re.sub(REGEX_TITLE, "", video.title) + FILE_EXTENSION

        Logger.info(LOG_TAG + "Downloading: " + title)        

        if not os.path.exists(OUTPUT):
            os.mkdir(OUTPUT)

        try:
            video.streams.get_audio_only().download(
                output_path=OUTPUT, 
                filename=title, 
                max_retries=3)           
             
            Logger.info(DOWNLOAD_SUCCESS)            
        except BaseException:            
            Logger.error(DOWNLOAD_ERROR, exc_info=traceback.format_exc())            

    def download_playlist(self, playlist):
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
        except BaseException:
            Logger.error(URL_ERROR, exc_info=traceback.format_exc())            

        self.downloading = False

    def is_playlist(self, url: str) -> bool:
        return url.find(URL_PLAYLIST_SUBSTR) != -1
