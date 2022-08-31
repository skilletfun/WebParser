import os
import sys
import json
import traceback
import subprocess

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyQt5.QtCore import pyqtSlot, QObject, QThread

from Worker import Worker


class Web_parser(QObject):
    SYMBOLS_FOR_DELETE = 7
    my_thread = None
    worker = None
    notifier = None
    config = {
        'save_folder': '',
        'remember_save_folder': True,
        'path_to_browser': '',
        'notifications': True,
        'requests_limit': 100,
        'semaphore_limit': 200,
        'download_tries': 10,
        'scroll_delay': 0.2,
        'version': 'v1.7'
    }

    def __init__(self):
        super(Web_parser, self).__init__()

        # Prepare logs
        if not os.path.exists('logs'):
            os.mkdir('logs')
        time_now = str(datetime.now()).replace(' ', '_').replace(':', '_')[:-7]
        self.log_file = f'logs/{time_now}.txt'

        # Notifier
        if not sys.platform.startswith("linux"):
            import win10toast
            self.SYMBOLS_FOR_DELETE = 8
            self.notifier = win10toast.ToastNotifier()

        # Load config
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                self.config.update(json.load(f))
        self.update_config_file()

    @pyqtSlot(str, int, str, str, bool, bool, str)
    def parse(self, url, timeout, save_folder, redownload_numbers, do_archive, do_merge, chapter_count):
        try:
            # Check given save_folder. Change it in 'config.json' if needed.
            if save_folder != '':
                self.config['save_folder'] = save_folder[self.SYMBOLS_FOR_DELETE:]
                self.update_config_file()

            self.notify_flag = True

            attrs = {
                'url': url,
                'timeout': timeout,
                'redownload_numbers': redownload_numbers,
                'do_archive': do_archive,
                'do_merge': do_merge,
                'chapter_count': chapter_count
            }

            # Start new thread to prevent freeze gui
            self.my_thread = QThread()
            self.worker = Worker(attrs, self)
            self.my_thread.started.connect(self.worker.run)
            self.worker.moveToThread(self.my_thread)
            self.my_thread.start()
        except Exception:
            with open(self.log_file, 'a') as file:
                traceback.print_exc(file=file)

    @pyqtSlot(result=str)
    def get_current_config(self):
        return json.dumps(self.config)

    @pyqtSlot(result=str)
    def get_version(self):
        return self.config['version']

    @pyqtSlot()
    @pyqtSlot(str)
    def update_config_file(self, config=None):
        if config:
            config = json.loads(config)
            self.config.update(config)
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    @pyqtSlot(result=str)
    def check_driver(self):
        """ Check the accuracy of setted up chromedriver. """
        res = ''
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("window-size=900,600")

            if not sys.platform.startswith("linux"): ex_path = 'chromedriver.exe'
            else: ex_path = 'chromedriver'

            browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
            browser.get('https://www.google.com')
            browser.close()
            browser.quit()
            res = 'True'
        finally:
            if res == '': return 'False'
            else: return res

    @pyqtSlot()
    def cancel_download(self):
        if self.worker:
            self.my_thread.terminate()
            self.my_thread.quit()
            self.my_thread = None
            self.worker.parser.quit_browser()
            self.worker = None

    @pyqtSlot(result=int)
    def get_total_images(self):
        """ Return the number of total images in chapter. """
        try:
            total_images = self.worker.parser.total_images
        except:
            total_images = 0
        return total_images

    @pyqtSlot(result=int)
    def get_total_download_images(self):
        """ Return the number of images that just downloaded. """
        try:
            total_download_images = self.worker.parser.total_download_images
        except:
            total_download_images = 0
        return total_download_images

    @pyqtSlot(result=str)
    def get_current_title(self):
        """ Return the title of current downloaded chapter. """
        try:
            current_title = self.worker.parser.current_title
        except:
            current_title = ''
        return current_title

    @pyqtSlot(result=str)
    def get_running(self):
        """ Check state of parser (download or not) at the moment. """
        try:
            running = self.worker.running
        except:
            running = False

        if not running and self.notify_flag and self.config['notifications']:
            self.notify_flag = False
            if not sys.platform.startswith("linux"):
                self.notifier.show_toast(title='WebParser', msg='Downloading all chapters complete',
                                         icon_path='res/icon.ico', threaded=True)
            else:
                os.system('notify-send "Downloading all chapters complete" "WebParser"')
        return str(running)

    @pyqtSlot(result=str)
    def get_browser_version(self):
        """ Return version of Google Chrome or Chromium. """
        # Windows
        if not sys.platform.startswith("linux"):
            try:
                arr = os.popen('reg query HKCU\\Software\\Google\\Chrome\\BLBeacon').read().split()
                i = arr.index('version')
            except:
                arr = os.popen('reg query HKCU\\Software\\Chromium\\BLBeacon').read().split()
                i = arr.index('version')
            version = arr[i + 2]
        else:
            # Linux            
            try:
                res = subprocess.check_output(['chromium', '--version'])
            except:
                res = subprocess.check_output(['google-chrome', '--version'])
            
            version = res.decode('utf-8').split()[1]
        return version

    @pyqtSlot()
    def download_chromedriver(self):
        """ Download correct chromedriver. If current version exists at site. """
        import requests as r
        from patoolib import extract_archive

        version_browser = self.get_browser_version().split('.')[0]
        version_driver_url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version_browser}'
        version_driver_full = r.get(version_driver_url).text

        if not sys.platform.startswith("linux"): this_os = 'win32'
        else: this_os = 'linux64'

        url = f'https://chromedriver.storage.googleapis.com/{version_driver_full}/chromedriver_{this_os}.zip'

        res = r.get(url, stream=True)
        name = 'chromedriver'

        with open(f'{name}.zip', 'wb') as fd:
            for chunk in res.iter_content(chunk_size=128):
                fd.write(chunk)

        if os.path.exists('chromedriver.exe'): os.remove('chromedriver.exe')
        elif os.path.exists('chromedriver'): os.remove('chromedriver')

        extract_archive(f'{name}.zip')
        os.remove(f'{name}.zip')

    @pyqtSlot()
    def show_log(self):
        """ Open log-file (in Windows basic app (Notepad)). """
        l_dir = os.listdir('logs')
        l_dir.sort()
        last_log = l_dir[-1]
        if not sys.platform.startswith("linux"):
            os.startfile(os.path.normpath(f'logs/{last_log}'))  # Windows
        else:
            subprocess.call(['xdg-open', f'logs/{last_log}'])  # Linux

    @pyqtSlot()
    def get_the_help(self):
        """ Show 'help.pdf'. """
        if not sys.platform.startswith("linux"):
            os.startfile(os.path.normpath('res/help.pdf'))  # Windows
        else:
            subprocess.call(['xdg-open', 'res/help.pdf'])  # Linux
