from PyQt5.QtCore import pyqtSlot, QObject


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


    @pyqtSlot()
    def run(self):
        self.running = True
#        
#        if self.save_folder.startswith("file://"):
#            self.save_folder = self.save_folder[self.countOfDeletedSymbols:]

        if self.url.startswith('file://'):
            self.url = self.url[self.countOfDeletedSymbols:]

            with open(self.url, "r") as f:
                urls = f.read().split('\n')
                urls.pop()
        else: urls = [self.url]

        if self.chapter_count == '':
            self.chapter_count = 1

        for url in urls:
            attrs = {'url': url, 'timeout': self.timeout, 'redownload_numbers': self.redownload_numbers,
            'do_archive': self.do_archive, 'do_merge': self.do_merge, 'chapter_count': self.chapter_count}

            if 'manga.bilibili.com' in url:
                from parsers.manga_bilibili_com import manga_bilibili_com
                self.parser = manga_bilibili_com(self.web_parser.config)
            elif 'webtoons.com' in url:
                from parsers.webtoons_com import webtoons_com
                self.parser = webtoons_com(self.web_parser.config)
            elif 'rawdevart.com' in url:
                from parsers.rawdevart_com import rawdevart_com
                self.parser = rawdevart_com(self.web_parser.config)
            elif 'webmota.com' in url or 'baozimh.com' in url:
                from parsers.webmota_com import webmota_com
                self.parser = webmota_com(self.web_parser.config)
            elif 'mangareader.to' in url:
                from parsers.mangareader_to import mangareader_to
                self.parser = mangareader_to(self.web_parser.config)
            elif 'fanfox.net' in url:
                from parsers.fanfox_net import fanfox_net
                self.parser = fanfox_net(self.web_parser.config)
            elif 'manhuadb.com' in url:
                from parsers.manhuadb import manhuadb_com
                self.parser = manhuadb_com(self.web_parser.config)
            elif 'page.kakao.com' in url:
                from parsers.page_kakao_com import page_kakao_com
                self.parser = page_kakao_com(self.web_parser.config)
            elif 'comic.naver.com' in url:
                from parsers.comic_naver_com import comic_naver_com
                self.parser = comic_naver_com(self.web_parser.config)
            elif 'kuaikanmanhua.com' in url:
                from parsers.kuaikanmanhua_com import kuaikanmanhua_com
                self.parser = kuaikanmanhua_com(self.web_parser.config)
            elif 'ac.qq.com' in url:
                from parsers.ac_qq_com import ac_qq_com
                self.parser = ac_qq_com(self.web_parser.config)
            elif 'mangakakalots.com' in url:
                from parsers.mangakakalots_com import mangakakalots_com
                self.parser = mangakakalots_com(self.web_parser.config)

            if not self.parser is None: self.parser.parse(attrs)
            self.running = False
