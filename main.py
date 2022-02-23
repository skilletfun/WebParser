# This Python file uses the following encoding: utf-8
import sys
import os

from Web_parser import Web_parser
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QThread

from asyncqt import QEventLoop
import asyncio

# pyinstaller main.py --icon=icon.ico --noconsole

""" Define necessary variables. """

ORGANIZATION_NAME = 'SkilletfunINC'
ORGANIZATION_DOMAIN = 'empty.com'
APPLICATION_NAME = 'MultiTool'
SETTINGS_TRAY = 'settings/tray'

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    loop = QEventLoop(app) # New
    asyncio.set_event_loop(loop) # New

    ctx = engine.rootContext()

    """ Set up the application. """
    
    app.setApplicationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(ORGANIZATION_DOMAIN)
    app.setApplicationName(APPLICATION_NAME)
    app.setWindowIcon(QIcon('res/icon.png'))

    web = Web_parser()
    
    """ If autoupdate is enabled -> """
    if web.config['auto_update']:
        import requests
        import subprocess
        import sys

        
        url = requests.get('https://github.com/skilletfun/WebParser/releases/latest')
        filename = 'update.zip'
        
        tag = url.url.split('/')[-1]
        
        """ If tags not equals. """
        if not tag == web.config['version']:
            base_url = 'https://github.com/skilletfun/WebParser/releases/download/'
            
            f = requests.get(base_url+tag+'/'+filename, stream=True)
            
            with open(filename, 'wb') as fd:
                for chunk in f.iter_content(chunk_size=128):
                    fd.write(chunk)
        
            web.config['version'] = tag
            web.update_config_file()
            
            if not sys.platform.startswith("linux"):
                theproc = subprocess.Popen('updater.exe')
                theproc.communicate()
            else:
                theproc = subprocess.Popen('python3 updater.py &', shell=True)
                theproc.communicate()
            sys.exit()

    ctx.setContextProperty("parser", web)

    """ Start app. """

    engine.load(os.path.join(os.path.dirname(__file__), "res/Web_parser.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    with loop:
        sys.exit(loop.run_forever())
