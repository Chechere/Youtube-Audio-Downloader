from varfile import *

import os, re, ssl, time, traceback, logging

from logging import LogRecord
from threading import Thread

from kivy.app import App, ObjectProperty
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.logger import Logger, LoggerHistory

from pytube import Playlist, YouTube
import certifi        

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
            self.label.color =  (1, 1, 1, 1)

        self.label.text = record.getMessage().removeprefix(LOG_TAG)
        print("HOla")          

class AppGrid(Widget):
    info_label: Label = ObjectProperty(None)
    text_input: TextInput = ObjectProperty(None)
    download_button: Button = ObjectProperty(None)

    background_app: Image

    def __init__(self, **kwargs):
        self.background_app: Image = Image(source=BG_IMAGE).texture               

        super().__init__(**kwargs)  

        Logger.addHandler(LogLabelHander(self.info_label))             

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

        # self.show_info(DOWNLOAD_PLAYLIST, INFO_COLOR)
        Logger.info(DOWNLOAD_PLAYLIST)        

    def download(self, url: str):
        try:
            if self.is_playlist(url):
                self.download_playlist(Playlist(url))
            else:
                self.download_video(YouTube(url))
        except BaseException:
            Logger.error(URL_ERROR, exc_info=traceback.format_exc())            

        self.download_button.disabled = False

    def is_playlist(self, url: str) -> bool:
        return url.find(URL_PLAYLIST_SUBSTR) != -1

    def button_click(self, instance):
        self.download_button.disabled = True

        Thread(
            target=self.download, 
            args=[self.text_input.text]).start()

    def save_log_click(self, instance):        
        if(not os.path.isdir(LOG_FOLDER)):            
            Logger.info(CREATING_FOLDER_LOG)            
            os.makedirs(LOG_FOLDER)                
        
        fh = logging.FileHandler(LOG_FILE_NAME_FORMAT)
        fh.setFormatter(logging.Formatter(LOG_MESSAGE_FORMAT))
        fh.setLevel(logging.DEBUG)        
        
        Logger.info(LOGGER_WRITTING_LOG_FILE)            

        log:LogRecord                                
        for log in reversed(LoggerHistory.history):
            fh.emit(log)

        Logger.info(LOG_SAVED)                    
        fh.emit(LoggerHistory.history[0])
            
class YTAudioDownloader(App):
    def build(self):
        self.title = TITLE
        self.icon = ICO_IMAGE        
        self.root = Builder.load_file(LAYOUT_FILE)                

        return AppGrid()

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_stdlib_context
    os.environ["SSL_CERT_FILE"] = certifi.where()    

    Config.set("graphics", "resizable", False)        

    try:
        app: YTAudioDownloader = YTAudioDownloader()
        app.run()
    except BaseException:
        print("ERROR! ", APP_ERROR)
        print(traceback.format_exc())

        fh = logging.FileHandler(LOG_FILE_NAME_FORMAT)
        fh.setFormatter(logging.Formatter(LOG_MESSAGE_FORMAT))
        fh.setLevel(logging.DEBUG)   

        fh.emit(LogRecord(level= logging.ERROR, name= APP_ERROR, msg= traceback.format_exc(), 
                exc_info= None, 
                pathname= None, 
                args= None, 
                lineno= None))