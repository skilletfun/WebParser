# This Python file uses the following encoding: utf-8
import sys
import os
from Web_parser import Web_parser
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine

# =====================================================================#
# Define necessary variables
# =====================================================================#

ORGANIZATION_NAME = 'SkilletfunINC'
ORGANIZATION_DOMAIN = 'empty.com'
APPLICATION_NAME = 'MultiTool'
SETTINGS_TRAY = 'settings/tray'

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()

    # =====================================================================#
    # Set up the application
    # =====================================================================#

    app.setApplicationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(ORGANIZATION_DOMAIN)
    app.setApplicationName(APPLICATION_NAME)
    app.setWindowIcon(QIcon('icon.png'))

    web = Web_parser()

    ctx.setContextProperty("parser", web)

    # =====================================================================#
    # Start app
    # =====================================================================#

    engine.load(os.path.join(os.path.dirname(__file__), "Web_parser.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
