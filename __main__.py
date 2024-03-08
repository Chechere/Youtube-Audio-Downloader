from __consts__ import *

import os, traceback, logging

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

from downloader import Downloader

from kivy.config import ConfigParser
from kivy.uix.settings import Settings

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
        self.downloader:Downloader = Downloader()                       

    def button_click(self, instance):
        if self.downloader.downloading:
            return

        Thread(
            target=self.downloader.download, 
            args=[self.text_input.text]).start()

    def save_log_click(self, instance):        
        if(not os.path.isdir(DEFAULT_LOG_FOLDER)):            
            Logger.info(CREATING_FOLDER_LOG)            
            os.makedirs(DEFAULT_LOG_FOLDER)                
        
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
        self.root = Builder.load_file(LAYOUTS_FILE)                
        self.use_kivy_settings = False                

        return AppGrid()
    
    def build_settings(self, settings: Settings):
        config = ConfigParser()
        config.read("./config.ini")

        settings.add_json_panel(
                        title= "Youtube Downloader", 
                        config= config, 
                        filename= "config.json")
        
        return super().build_settings(settings)

def create_ini_file():
    with open(INI_FILE_DIR, "w") as f:        
        f.write("[FOLDERS]")
        f.write("\nLOG_FOLDER = " + DEFAULT_LOG_FOLDER)
        f.write("\nOUTPUT_FOLDER = " + DEFAULT_OUTPUT_FOLDER)        


if __name__ == "__main__":    
    if not os.path.isfile(INI_FILE_DIR):
        create_ini_file()
        pass

    # ! ERROR config.read_file(INI_FILE_DIR)

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

        fh.emit(LogRecord(level= logging.ERROR, name= APP_ERROR, msg= traceback.format_exc(), 
                exc_info= None, 
                pathname= None, 
                args= None, 
                lineno= None))