from PyQt5.QtCore import pyqtSlot, QObject
import time


class Worker(QObject):
    def __init__(self, url, timeout, redownload_numbers, do_archive, do_merge, chapter_count, web_parser):
        super(Worker, self).__init__()
        self.url = url
        self.timeout = timeout
        self.redownload_numbers = redownload_numbers
        self.do_archive = do_archive
        self.do_merge = do_merge
        self.chapter_count = chapter_count
        self.countOfDeletedSymbols = web_parser.countOfDeletedSymbols
        self.web_parser = web_parser
        self.parser = None

        self.sites = [
            'ac.qq.com', 'bomtoon.com', 'comic.naver.com', 'comico.kr', 'fanfox.net', 'kuaikanmanhua.com',
            'manga.bilibili.com', 'mangakakalots.com', 'mangareader.to', 'manhuadb.com', 'scansnelo.com',
            'page.kakao.com', 'rawdevart.com', 'ridibooks.com', 'webmota.com (baozihm.com)', 'webtoons.com'
        ]


    @pyqtSlot()
    def run(self):
        self.running = True

        if self.url.startswith('file://'):
            self.url = self.url[self.countOfDeletedSymbols:]

            with open(self.url, "r") as f:
                urls = f.read().split('\n')
                if urls[-1] == '\n' or urls[-1] == '': urls.pop()
        else: urls = [self.url]

        if self.chapter_count == '':
            self.chapter_count = 1

        for url in urls:
            attrs = {'url': url, 'timeout': self.timeout, 'redownload_numbers': self.redownload_numbers,
            'do_archive': self.do_archive, 'do_merge': self.do_merge, 'chapter_count': self.chapter_count}

            for site in self.sites:
                _site = site.replace('.', '_')
                if site in url:
                    exec(f'from parsers.{_site} import {_site}')
                    exec(f'self.parser = {_site}(self.web_parser.config)')
                    break

            if not self.parser is None:
                try:
                    self.parser.parse(attrs)
                except Exception as e:
                    self.web_parser.save_to_log(e)
            time.sleep(1)
        self.running = False
