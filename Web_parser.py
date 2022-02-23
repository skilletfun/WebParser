import sys
from PyQt5.QtCore import pyqtSlot, QObject, QThread
import json
import os
import subprocess
from datetime import datetime
from res.Worker import Worker


class Web_parser(QObject):
    countOfDeletedSymbols = 7

    my_thread = None
    worker = None

    old_stdout = None
    log_file = None

    notifier = None

    # Config
    config = {
        'save_folder': '',
        'remember_save_folder': True,
        'path_to_browser': '',
        'notifications': True,
        'requests_limit': 100,
        'semaphore_limit': 200,
        'download_tries': 5,
        'auto_update': False,
        'version': ''
    }


    def __init__(self):
    """Init: create log file, redirect all print to log file, load config. """
        
        super(Web_parser, self).__init__()

        self.old_stdout = sys.stdout
        self.log_file = open('logs/log.txt', 'w')
        sys.stdout = self.log_file

        self.save_to_log('Init WebParser')

        if not sys.platform.startswith("linux"):
            self.countOfDeletedSymbols = 8
            self.save_to_log('Init Notifier...')
            import win10toast
            self.notifier = win10toast.ToastNotifier()


        self.save_to_log('Open "config.json"...')

        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    file = json.load(f)
                    self.config.update(file)

            self.update_config_file()
            self.save_to_log('"Config.json" had been loaded')
        except Exception as e:
            self.save_to_log('Error while load "config.json"')
            self.save_to_log(e)
        self.save_to_log('Init WebParser complete')


    def __del__(self):        
        self.save_to_log('Close log')
        self.log_file.close()
        
        time_now = str(datetime.now()).replace(' ', '_')[:-7]
        os.rename('logs/log.txt', f'logs/{time_now}.txt')


    @pyqtSlot(str, int, str, str, bool, bool, str)
    def parse(self, url, timeout, save_folder, redownload_numbers, do_archive, do_merge, chapter_count):
    """ Main function. Parsing. """
    
        self.save_to_log('Start parsing...')
        
        # Check given save_folder. Change it in 'config.json' if needed
        if save_folder != '':
            self.config['save_folder'] = save_folder[self.countOfDeletedSymbols:]
            self.update_config_file()

        self.notify_flag = True

        # Start new thread to prevent freeze gui
        self.my_thread = QThread()
        self.worker = Worker(url, timeout, redownload_numbers, do_archive, do_merge, chapter_count, self)
        self.my_thread.started.connect(self.worker.run)
        self.worker.moveToThread(self.my_thread)
        self.my_thread.start()


    @pyqtSlot(result=str)
    def get_current_config(self):
    """ Return current config in string. """
    
        return json.dumps(self.config)


    @pyqtSlot()
    @pyqtSlot(str)
    def update_config_file(self, config=None):
    """ Update 'config.json'. Rewrite file. """
    
        self.save_to_log('Update "config.json"')
        try:
            if not config is None:
                self.save_to_log('JSON: ' + config)
                config = json.loads(config)
                self.config.update(config)
            with open('config.json', 'w') as f:
                json.dump(self.config, f)
        except Exception as e:
            self.save_to_log('Error while update "config.json"')
            self.save_to_log(e)


    @pyqtSlot(result=str)
    def check_driver(self):
    """ Check the accuracy of setted up chromedriver. """
    
        self.save_to_log('Check driver')
        res = ''
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

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
    """ Close the thread. Can be used for cancel downloading. """
    
        self.save_to_log('Cancel download / Finish download')
        self.my_thread.quit()


    @pyqtSlot(result=int)
    def get_total_images(self):
    """ Return the number of total images in chapter. """
    
        total_images = 0
        try:
            total_images = self.worker.parser.total_images
        except:
            pass
        return total_images


    @pyqtSlot(result=int)
    def get_total_download_images(self):
    """ Return the number of images that just downloaded. """
    
        total_download_images = 0
        try:
            total_download_images = self.worker.parser.total_download_images
        except:
            pass
        return total_download_images


    @pyqtSlot(result=str)
    def get_current_title(self):
    """ Return the title of current downloaded chapter. """
    
        current_title = ''
        try:
            current_title = self.worker.parser.current_title
        except:
            pass
        return current_title


    @pyqtSlot(result=str)
    def get_running(self):
    """ Check state of parser (download or not) at the moment. """
    
        running = False
        try:
            running = self.worker.running
        except:
            pass

        if not running and self.notify_flag and self.config['notifications']:
            self.notify_flag = False
            if not sys.platform.startswith("linux"):
                self.notifier.show_toast(title='WebParser', msg='Downloading all chapters complete', threaded=True)
            else:
                os.system('notify-send "Downloading all chapters complete" "WebParser"')
        return str(running)


    @pyqtSlot(result=str)
    def get_browser_version(self):
    """ Return version of Google Chrome or Chromium. """
    
        self.save_to_log('Try to get version of browser')
        
        # Windows
        if not sys.platform.startswith("linux"):
            try:
                arr = os.popen('reg query HKCU\\Software\\Google\\Chrome\\BLBeacon').read().split()
                i = arr.index('version')
            except Exception as e:
                self.save_to_log(e)
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

        self.save_to_log('Version of your browser: ' + version)
        return version


    @pyqtSlot()
    def download_chromedriver(self):
    """ Download correct chromedriver. """
    
        self.save_to_log('Try download chromedriver...')
        try:
            import requests as r
            from patoolib import extract_archive

            version = self.get_browser_version()
            url = f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip'
            res = r.get(url, stream=True)
            name = 'chromedriver'

            with open(f'{name}.zip', 'wb') as fd:
                for chunk in res.iter_content(chunk_size=128):
                    fd.write(chunk)

            extract_archive(f'{name}.zip')
            os.remove(f'{name}.zip')
            self.save_to_log('Downloading complete')
        except Exception as e:
            self.save_to_log('Error while downloading')
            self.save_to_log(e)


    @pyqtSlot(str)
    def save_to_log(self, log):
    """ Save information to log-file. """
    
        print('Log:', log)
        print()


    @pyqtSlot()
    def show_log(self):
    """ Open log-file (in Windows basic app (Notepad)). """
    
        self.save_to_log('Open last log...')
        try:
            l_dir = os.listdir('logs')
            l_dir.sort()
            
            if 'log.txt' in l_dir:
                l_dir.remove('log.txt')
            
            last_log = l_dir[-1]
            
            self.save_to_log('Last log: ' + last_log)

            if not sys.platform.startswith("linux"):
                # Windows
                os.startfile(os.path.normpath(f'logs/{last_log}'))   
            else:
                # Linux
                subprocess.call(['xdg-open', f'logs/{last_log}']) 
        except Exception as e:
            self.save_to_log('Error while open "log_last.txt"')
            self.save_to_log(e)


    @pyqtSlot()
    def get_the_help(self):
    """ Show 'help.pdf'. """
    
        self.save_to_log('Open "help.pdf"...')
        try:            
            if not sys.platform.startswith("linux"):
                # Windows
                os.startfile(os.path.normpath('res/help.pdf'))
            else:
                # Linux
                subprocess.call(['xdg-open', 'res/help.pdf'])
        except Exception as e:
            self.save_to_log('Error while open "help.pdf"')
            self.save_to_log(e)
