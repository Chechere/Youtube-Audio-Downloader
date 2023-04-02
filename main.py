import os, re, ssl, time, traceback
import certifi
from threading import Thread
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.config import Config
from pytube import Playlist, YouTube

if (platform == 'android'):
    from android.storage import primary_external_storage_path
    from android.permissions import Permission, request_permissions


class MyApp(App):
    def show_info(self, info, type='info'):
        if (type == 'error'):
            self.root.ids.info_label.color = (1, 0, 0, 1)
        else:
            self.root.ids.info_label.color = (0, 1, 0, 1)

        self.root.ids.info_label.text = info

    def download_video(self, video):
        title = re.sub(r'([^a-zA-Z0-9\s\.\-_áéíóú])+',
                       '', video.title) + '.mp3'

        output = './'
        if (platform == 'android'):
            output = os.path.join(primary_external_storage_path(), 'Download')

        self.show_info('Downloading: ' + title)

        try:
            video.streams.get_audio_only().download(
                output_path=output, filename=title, max_retries=3)
            self.show_info('Download Success!')
        except BaseException as ex:
            # show_info('Download_video: ' + traceback.format_exc(), 'error')
            self.show_info('Error downloading music', 'error')

    def download_playlist(self, playlist):
        download_fails = 0

        for video in playlist.videos:
            self.download_video(video)
            time.sleep(1.5)

        self.show_info('Playlist downloaded')

    def download(self, url):
        try:
            if (url.find('playlist?list=') != -1):
                self.download_playlist(Playlist(url))
            else:
                self.download_video(YouTube(url))
        except BaseException as ex:
            self.show_info(
                'Error getting video or playlist. Please, check URL', 'error')
            # show_info('Download: ' + repr(ex), 'error')

    def button_click(self, instance):
        Thread(target=self.download, args=[self.root.ids.input.text]).start()

    def build(self):
        self.texture = Image(source='assets/background.jpeg').texture
        self.texture.wrap = 'repeat'
        self.texture.uvsize = (8, -1)

        return Builder.load_file('layout.kv')


if __name__ == '__main__':
    if (platform == 'android'):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,
                            Permission.INTERNET, Permission.ACCESS_NETWORK_STATE, Permission.ACCESS_WIFI_STATE])

    ssl._create_default_https_context = ssl._create_stdlib_context
    os.environ['SSL_CERT_FILE'] = certifi.where()

    Config.set('kivy', 'window_icon', 'assets/icon.png')

    MyApp().run()
