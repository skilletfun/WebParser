# This Python file uses the following encoding: utf-8
import sys
import os

from Web_parser import Web_parser
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QThread

from asyncqt import QEventLoop
import asyncio

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

    ctx.setContextProperty("parser", web)

    """ Start app. """

    engine.load(os.path.join(os.path.dirname(__file__), "res/Web_parser.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    with loop:
        sys.exit(loop.run_forever())
