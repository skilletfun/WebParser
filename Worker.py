import time

from PyQt5.QtCore import pyqtSlot, QObject
from selenium.webdriver.common.by import By

from parsers.basic_parser import basic_parser
from utils.logging import log
from utils.browser import Browser
from config import SYMBOLS_FOR_DELETE


class Worker(QObject):
    def __init__(self, url, chapters_count) -> None:
        super(Worker, self).__init__()
        self.url = url
        self.chapters_count = chapters_count

        self.SITES = {
            'ac.qq.com': None,
            'bomtoon.com': None,
            'comic.naver.com': None,
            'comico.kr': None,
            'fanfox.net': None,
            'kuaikanmanhua.com': None,
            'manga.bilibili.com': None,
            'mangakakalot.com': None,
            'mangareader.to': None,
            'manhuadb.com': None,
            'mechacomic.jp': None,
            'scansnelo.com': None,
            'page.kakao.com': self.page_kakao_com,
            'rawdevart.com': None,
            'ridibooks.com': None,
            'webmota.com': None,
            'webtoons.com': None
        }

    @pyqtSlot()
    def run(self) -> None:
        self.running = True
        if self.url.startswith('file://'):
            self.url = self.url[SYMBOLS_FOR_DELETE:]

            with open(self.url, "r") as f:
                urls = f.read().split('\n')
                if urls[-1] in ['\n', '']:
                    urls.pop()
        else:
            urls = [self.url]

        for url in urls:
            self.main_parse(url)
        self.running = False

    @log
    def main_parse(self, url: str) -> None:
        """ Находит соответствующий парсер и запускает парсинг. """
        for site in self.SITES.keys():
            if site in url:
                browser = Browser()
                time.sleep(0.5)
                self.SITES[site](browser, url)
                break
        time.sleep(1)

    @log
    def try_next_chapter(self, browser, script_next_chapter, title, script_title=None):
        """ Попытка загрузить следующую главу. """
        old_title = title
        browser.execute(script_next_chapter)
        max_wait = 10
        time.sleep(5)
        while title == old_title and max_wait > 0:
            title = browser.execute(script_title) if script_title else browser.title
            max_wait -= 1
            time.sleep(1)

    @log
    def page_kakao_com(self, browser: Browser, url: str) -> None:
        old_title = ''
        self.parser = basic_parser()
        url, self.chapters_count, step = self.parser.fix_vars(url, self.chapters_count)
        browser.get(url)
        while True:
            self.chapters_count -= step
            title = browser.execute("return document.title;")
            if title == old_title: break
            images = browser.execute("return document.getElementsByClassName('css-3q7n7r-ScrollImageViewerImage');")
            images = [el.get_attribute('src') for el in images]
            self.parser.full_download(images, title)
            if self.chapters_count > 0:
                s_next = "document.getElementsByClassName('linkItem')[3].click();"
                s_title = "return document.title;"
                self.try_next_chapter(browser, s_next, title, s_title)
            else: break
        browser.shutdown()
