import sys

from PyQt5.QtCore import pyqtSlot, QObject

from parsers import webtoons_com, fanfox_net
from parsers import manga_bilibili_com, webmota_com, manhuadb
from parsers import rawdevart_com, mangareader_to, page_kakao_com


class Web_parser(QObject):
    countOfDeletedSymbols = 7

    def __init__(self):
        super(Web_parser, self).__init__()
        if not sys.platform.startswith("linux"):
            self.countOfDeletedSymbols = 8

    @pyqtSlot(result=str)
    def check_driver(self):
        res = ''
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("window-size=900,600")

            if not sys.platform.startswith("linux"):
                ex_path = 'chromedriver.exe'
            else:
                ex_path = 'chromedriver'

            browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)

            browser.get('https://www.google.com')
            browser.close()
            browser.quit()
            res = 'True'
        finally:
            if res == '':
                return 'False'
            else:
                return res


    @pyqtSlot(str, int, str, str, bool, str)
    def parse(self, url, timeout, save_folder, redownload_imgs, do_archive, chapter_count):
        if save_folder.startswith("file://"):
            save_folder = save_folder[self.countOfDeletedSymbols:]

        if url.startswith('file://'):
            url = url[self.countOfDeletedSymbols:]

            with open(url, "r") as f:
                urls = f.read().split('\n')
                urls.pop()
        else:
            urls = [url]

        if chapter_count == '':
            chapter_count = 1

        attrs = [url, timeout, save_folder, redownload_imgs, do_archive, chapter_count]

        for url in urls:
            if 'manga.bilibili.com' in url:
                manga_bilibili_com.parse(*attrs)
            elif 'webtoons.com' in url:
                webtoons_com.parse(*attrs)
            elif 'rawdevart.com' in url:
                 rawdevart_com.parse(*attrs)
            elif 'webmota.com' in url:
                webmota_com.parse(*attrs)
            elif 'mangareader.to' in url:
                mangareader_to.parse(*attrs)
            elif 'fanfox.net' in url:
                fanfox_net.parse(*attrs)
            elif 'manhuadb.com' in url:
                manhuadb.parse(*attrs)
            elif 'page.kakao.com' in url:
                path_to_browser = self.get_path_to_browser()
                page_kakao_com.parse(*attrs, path_to_browser)

    @pyqtSlot(result=str)
    def get_path_to_browser(self):
        with open('path_to_browser.txt', 'r') as f:
            path_to_browser = f.read()
            f.close()
            return path_to_browser

    @pyqtSlot(str)
    def set_path_to_browser(self, path_to_browser):
        with open('path_to_browser.txt', 'w') as f:
            f.write(path_to_browser)
            f.close()