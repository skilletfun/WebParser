import time

from PyQt5.QtCore import pyqtSlot, QObject

from utils.logging import log


class Worker(QObject):
    def __init__(self, attrs, web_parser) -> None:
        super(Worker, self).__init__()

        self.attrs = attrs
        self.SYMBOLS_FOR_DELETE = web_parser.SYMBOLS_FOR_DELETE
        self.web_parser = web_parser
        self.parser = None

        self.sites = [
            'ac.qq.com',
            'bomtoon.com',
            'comic.naver.com',
            'comico.kr',
            'fanfox.net',
            'kuaikanmanhua.com',
            'manga.bilibili.com',
            'mangakakalot.com',
            'mangareader.to',
            'manhuadb.com',
            'mechacomic.jp',
            'scansnelo.com',
            'page.kakao.com',
            'rawdevart.com',
            'ridibooks.com',
            'webmota.com',
            'webtoons.com'
        ]

    @pyqtSlot()
    def run(self) -> None:
        try:
            self.running = True
            if self.attrs['url'].startswith('file://'):
                self.attrs['url'] = self.attrs['url'][self.SYMBOLS_FOR_DELETE:]

                with open(self.attrs['url'], "r") as f:
                    urls = f.read().split('\n')
                    if urls[-1] in ['\n', '']:
                        urls.pop()
            else:
                urls = [self.attrs['url']]

            if self.attrs['chapter_count'] == '':
                self.attrs['chapter_count'] = 1

            for url in urls:
                self.parse(url)
            self.running = False
        except Exception as e:
            raise e

    @log
    def parse(self, url: str) -> None:
        """ Import neccessary parser and start parse. """

        self.attrs['url'] = url
        for site in self.sites:
            _site = site.replace('.', '_')
            if site in url:
                exec(f'from parsers.{_site} import {_site}')
                exec(f'self.parser = {_site}(self.web_parser.config)')
                break

        if self.parser:
            self.parser.parse(self.attrs)

        time.sleep(1)
