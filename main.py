# This Python file uses the following encoding: utf-8
import os
import sys
import asyncio

from asyncqt import QEventLoop
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QThread

from Web_parser import Web_parser


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    ctx = engine.rootContext()

    app.setApplicationName('SkilletfunINC')
    app.setOrganizationDomain('empty.com')
    app.setApplicationName('MultiTool')
    app.setWindowIcon(QIcon('res/icons/icon.png'))

    web = Web_parser()

    ctx.setContextProperty("parser", web)

    engine.load(os.path.join(os.path.dirname(__file__), "res/qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    with loop:
        sys.exit(loop.run_forever())
