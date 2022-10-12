import os
import sys

from PyQt5.QtCore import pyqtSlot, QObject, QThread

from Worker import Worker
import config


class Web_parser(QObject):
    my_thread = None    # Поток, в котором происходит парсинг
    worker = None       # Объект, который занимается парсингом
    notifier = None     # Объект, который посылает уведомления

    def __init__(self) -> None:
        super(Web_parser, self).__init__()
        # Если текущая ОС - не линукс, то импортируем доп-пакет
        if not sys.platform.startswith("linux"):
            import win10toast
            self.notifier = win10toast.ToastNotifier()

    @pyqtSlot(str, str)
    def parse(self, url: str, chapters_count: str) -> None:
        """ Точка входа в парсинг. 
        :param url: ссылка на главу
        :param chapters_count: количество глав для скачки
        """
        self.notify_flag = True
        self.my_thread = QThread()
        self.worker = Worker(url, chapters_count)
        self.my_thread.started.connect(self.worker.run)
        self.worker.moveToThread(self.my_thread)
        self.my_thread.start()

    @pyqtSlot(result=str)
    def get_version(self) -> str:
        """ Возвращает текущую версию программы. """
        return config.VERSION

    @pyqtSlot()
    def cancel_download(self) -> None:
        """ Прерывает загрузку. """
        if self.worker:
            self.my_thread.quit()
            self.my_thread = None
            self.worker = None

    @pyqtSlot(result=int)
    def get_total_images(self) -> int:
        """ Возвращает количество сканов, которое необходимо загрузить. """
        try:
            total_images = self.worker.parser.total_images
        except:
            total_images = 0
        return total_images

    @pyqtSlot(result=int)
    def get_total_download_images(self) -> int:
        """ Возвращает количество скачанных сканов. """
        try:
            total_download_images = self.worker.parser.total_download_images
        except:
            total_download_images = 0
        return total_download_images

    @pyqtSlot(result=str)
    def get_current_title(self) -> str:
        """ Возвращает название главы, которая скачивается. """
        try:
            current_title = self.worker.parser.current_title
        except:
            current_title = ''
        return current_title

    @pyqtSlot(result=str)
    def get_running(self) -> str:
        """ Проверяет, идет ли в данный момент загрузка. """
        try:
            running = self.worker.running
        except:
            running = False

        if not running and self.notify_flag and config.NOTIFY:
            self.notify()
        return str(running)

    def notify(self) -> None:
        """ Отправляет уведомление о завершении работы. """
        self.notify_flag = False
        if not sys.platform.startswith("linux"):
            self.notifier.show_toast(title='WebParser', msg='Downloading complete',
                                        icon_path='res/icons/icon.ico', threaded=True)
        else:
            os.system('notify-send "Downloading complete" "WebParser"')
