import json
import time
from typing import Callable, Optional, Tuple

from PyQt5.QtCore import pyqtSlot, QObject
from selenium.webdriver.common.by import By

from utils.logging import log
from utils.browser import Browser
from basic_parser import basic_parser
from config import SYMBOLS_FOR_DELETE, NEW_REMANGA


class Worker(QObject):
    def __init__(self, url: str, chapters_count: str) -> None:
        super(Worker, self).__init__()
        self.url = 'https://' + url if not (url.startswith('http') or url.startswith('file://')) else url
        self.chapters_count, self.step = self.fix_chapter_count(chapters_count)

        self.SITES = {
            'ac.qq.com': self.ac_qq_com,
            'bomtoon.com': None,
            'comic.naver.com': self.comic_naver_com,
            'comico.kr': None,
            'fanfox.net': None,
            'kuaikanmanhua.com': self.kuaikanmanhua_com,
            'king-manga.com': self.king_manga_com,
            'manga.bilibili.com': None,
            'mangakakalot.com': self.mangakakalot_com,
            'mangareader.to': None,
            'manhuadb.com': None,
            'mechacomic.jp': self.mechacomic_jp,
            'page.kakao.com': self.page_kakao_com,
            'rawdevart.com': self.rawdevart_com,
            'remanga.org': self.remanga_org,
            'ridibooks.com': self.ridibooks_com,
            'webmota.com': self.webmota_com,
            'webtoons.com': self.webtoons_com
        }

    @pyqtSlot()
    def run(self) -> None:
        self.running = True
        if self.url.startswith('file://'):
            self.url = self.url[SYMBOLS_FOR_DELETE:]
            with open(self.url, "r") as f:
                urls = f.read().split('\n')
                if urls[-1] in ['\n', '']: urls.pop()
        else: urls = [self.url]
        browser = None
        try:
            for url in urls:
                counter = self.chapters_count # Счетчик обнуляется для каждой новой ссылки (если указан файл со ссылками)
                for site in self.SITES.keys():
                    if site in url:
                        if not browser:
                            browser = Browser()
                        time.sleep(0.5)
                        # Будут парситься главы по порядку до тех пор, пока не появится битая ссылка или не кончится счетчик 
                        while url and counter:
                            url = self.SITES[site](browser, url)
                            counter -= self.step
                        time.sleep(1)
                        break
                time.sleep(1)
        finally:
            if browser: browser.shutdown()
        self.running = False

    @log
    def fix_chapter_count(self, chapter_count: str) -> Tuple[int, int]:
        """ Преобразует строку с количеством глав в корректный вид и
        возвращает количество глав и шаг, на который оно будет уменьшаться. """
        if chapter_count != '*':
            chapter_count = 1 if chapter_count == '' else int(chapter_count)
            step = 1
        else:
            step = 0
            chapter_count = 1
        return chapter_count, step

    @log
    def base_bs_parse(self, url: str, get_images: Callable, tag: str, break_check: Callable, browser: Browser=None):
        """ Запрашивает страницу, а затем сохраняет картинки, запрашивая их через ссылки в разметке.
        :param url: ссылка на страницу (главу)
        :param get_images: лямбда, которая получит ссылки на картинки в html-разметке
        :param tag: свойство, в котором находится ссылка на картинку (обычно <src>)
        :param break_check: лямбда, которая проверит, нужно ли качать эту страницу (дубликат)
        :param browser: объект браузера, если нужно отрендерить js перед поиском ссылок
        """
        self.parser = basic_parser()
        src = self.parser.get_response(url) if not browser else browser.get(url)
        if break_check(): return False
        title, images = get_images(src)
        images = [el.get(tag).strip() for el in images if el.get(tag)]
        self.parser.full_download(images, title)
        return src

    @log
    def base_driver_parse(
        self,
        url: str,
        browser: Browser,
        reqs_filter: str,
        filtered_images: Callable,
        scroll_element: str=None,
        scroll_check: Callable=None,
        script_after_load: Callable=None
    ) -> bool:
        """ Прогружает страницу в браузере, а затем сохраняет картинки, полученые через запросы, перехватывая их.
        :param url: ссылка на страницу (главу)
        :param browser: объект уже запущенного браузера
        :param reqs_filter: строка, с которой должны начинаться запросы к картинкам (по ней произойдет фильтрация)
        :param filtered_images: лямбда, которая получит ссылки на картинки в html-разметке
        :param scroll_element: строка (js-код), который представляет путь до прокручиваемых элементов
        :param scroll_check: лямбда, которая проверит, прогружен ли элемент
        """
        self.parser = basic_parser()
        browser.get(url)
        time.sleep(3)
        if script_after_load: script_after_load()
        self.parser.current_title = browser.execute("return document.title;")
        if scroll_check and scroll_element:
            browser.scroll_page(scroll_element, scroll_check) # Прокрутка страницы
        reqs = browser.wait_reqs(reqs_filter)
        self.parser.total_images = len(reqs)
        images_in_bytes = self.compare_images(filtered_images(), reqs)
        browser.save_images_from_bytes(self.parser.prepare_save_folder(self.parser.current_title), images_in_bytes)
        return True

    @log
    def compare_images(self, urls: list, reqs: list) -> list:
        """ Находит среди запросов соответствующий картинке в разметке запрос, получая байты этого запроса. """
        res = []
        for i in range(len(urls)):
            for j in range(len(reqs)):
                if urls[i] in reqs[j].url:
                    res.append(reqs[j].response.body)
                    reqs.pop(j)
                    break
        return res

    #                   ---------------------------------
    #                   ----------   PARSERS   ----------
    #                   ---------------------------------

    @log
    def remanga_org(self, browser: Browser, url: str) -> Optional[str]:
        if NEW_REMANGA:
            script = "return document.getElementsByClassName('content')[0].getElementsByTagName('img');" 
        else:
            script = "return document.getElementById('app').getElementsByTagName('img');" 
        images = lambda: [el.get_attribute('src') for el in browser.execute(script)][:-1]
        flag = self.base_driver_parse(url, browser, 'https://', images)
        return '' if flag else None

    @log
    def manhuadb_com(self, browser: Browser, url: str) -> Optional[str]:
        ...

    @log
    def page_kakao_com(self, browser: Browser, url: str) -> Optional[str]:
        script = "return document.getElementsByClassName('css-3q7n7r-ScrollImageViewerImage');"
        images = lambda: [el.get_attribute('src') for el in browser.execute(script)]
        flag = self.base_driver_parse(url, browser, 'https://page-edge.kakao.com/sdownload', images)
        part_url = json.loads(browser.execute("return document.getElementsByClassName('css-1gzfypn-ViewerNavbarMenu')[0].getAttribute('data-t-obj');"))['eventMeta']['id']
        title = json.loads(browser.execute("return document.getElementById('__NEXT_DATA__').text;"))['props']['pageProps']['seriesId']
        return f'https://page.kakao.com/content/{title}/viewer/' + part_url if flag else None

    @log
    def ac_qq_com(self, browser: Browser, url: str) -> Optional[str]:
        script = "document.getElementById('comicContain').getElementsByTagName('img')"
        scroll_check = lambda j: browser.execute('return '+script + f'[{j}].getAttribute("class");') not in ['loaded', 'network-slow'] and \
                                 browser.execute('return '+script + f'[{j}].getAttribute("id");') != 'adTop'
        images = lambda: [el.get_attribute('src') for el in browser.execute('return '+script+';')]
        flag = self.base_driver_parse(url, browser, 'https://manhua.acimg.cn/manhua_detail/', images, script, scroll_check)
        return browser.execute("return document.getElementById('nextChapter').href;") if flag else None

    @log
    def webtoons_com(self, browser: Browser, url: str) -> Optional[str]:
        self.parser = basic_parser()
        src = browser.get(url)
        self.parser.current_title, images = self.parser.find_images(src, 'div', 'id', '_imageList')
        images = [img.get('data-url') for img in images]
        reqs = browser.wait_reqs('https://webtoon-phinf.pstatic.net')
        images_in_bytes = self.compare_images(images, reqs)
        browser.save_images_from_bytes(self.parser.prepare_save_folder(self.parser.current_title), images_in_bytes)
        res = self.parser.find_element(src, 'a', 'class', '_nextEpisode').get('href')
        return res if res else None

    @log
    def mangakakalot_com(self, browser: Browser, url: str) -> Optional[str]:
        self.parser = basic_parser()
        src = browser.get(url)
        self.parser.current_title, images = self.parser.find_images(src, 'div', 'class', 'container-chapter-reader')
        images = [img.get('src') for img in images]
        reqs = browser.wait_reqs('https://')
        images_in_bytes = self.compare_images(images, reqs)
        browser.save_images_from_bytes(self.parser.prepare_save_folder(self.parser.current_title), images_in_bytes)
        res = browser.execute("return document.getElementsByClassName('back')[0].href;")
        return res if res else None

    @log
    def comic_naver_com(self, browser: Browser, url: str) -> Optional[str]:
        if 'weekday' in url:
            url = url[:url.find('weekday') - 1]
        get_images = lambda src: self.parser.find_images(src, 'div', 'class', 'wt_viewer')
        self.base_bs_parse(url, get_images, 'src', lambda: 'list?titleId' in browser.current_url(), browser)
        return url[:url.rfind('=') + 1] + str(int(url[url.rfind('=') + 1:]) + 1)

    @log
    def webmota_com(self, browser: Browser, url: str) -> Optional[str]:
        get_images = lambda src: self.parser.find_images(src, 'ul', 'class', 'comic-contain', tag='amp-img')
        page_src = self.base_bs_parse(url, get_images, 'src', lambda: False)
        res = self.parser.find_element(page_src, 'div', 'class', 'bottom-bar-tool').find_all('a')[3].get('href')
        return res if res else None

    @log
    def king_manga_com(self, browser: Browser, url: str) -> Optional[str]:
        get_images = lambda src: self.parser.find_images(src, 'div', 'class', 'reading-content')
        page_src = self.base_bs_parse(url, get_images, 'src', lambda: False)
        res = self.find_element(page_src, 'a', 'class', 'next_page').get('href')
        return res if res else None

    @log
    def kuaikanmanhua_com(self, browser: Browser, url: str) -> Optional[str]:
        get_images = lambda src: self.parser.find_images(src, 'div', 'class', 'imgList')
        page_src = self.base_bs_parse(url, get_images, 'data-src', lambda: False, browser)
        res = self.parser.find_element(page_src, 'div', 'class', 'AdjacentChapters').find_all('a')[-1]
        return 'https://www.kuaikanmanhua.com' + res.get('href') if 'javascript' not in res else None

    @log
    def rawdevart_com(self, browser: Browser, url: str) -> None:
        self.parser = basic_parser()
        src = self.parser.get_response(url)
        title, images = self.parser.find_images(src, 'div', 'id', 'img-container')
        images = [img.get('data-src') for img in images]
        self.parser.full_download(images, title)

    @log
    def ridibooks_com(self, browser: Browser, url: str) -> Optional[str]:
        script = "document.getElementsByClassName('comic_page lazy_load')"
        scroll_check = lambda j: 'loaded' not in browser.execute('return ' + script + f'[{j}].classList;')
        images = lambda: [el.find_element(By.TAG_NAME, 'img').get_attribute('src') for el in browser.execute('return '+script+';')]
        flag = self.base_driver_parse(url, browser, 'https://webview-cache', images, script, scroll_check)
        js = browser.execute("return document.getElementsByTagName('script');")
        js = [el for el in js if el.get_property('textContent').strip().startswith('window.dispatchEvent')][0].get_property('textContent').strip()
        js = js[js.find('next_book'):]
        js = js[:js.find(',')-1]
        js = js[js.rfind('"')+1:]
        new_url = 'https://view.ridibooks.com/books/' + js
        return new_url if flag else None

    @log
    def mechacomic_jp(self, browser: Browser, url: str) -> None:
        self.parser = basic_parser()
        browser.get(url)
        browser.execute("document.getElementsByClassName('TutorialDialog__Close-sc-1w8lkht-1')[0].click();")
        self.parser.current_title = browser.execute("return document.title;")
        binaries = []
        script = "document.getElementsByClassName('PageContainer__Image-sc-13sb3i-5')"
        for i, el in enumerate(browser.execute('return '+script+';')):
            browser.execute(script + f'[{i}].scrollIntoView();')
            while not el.get_attribute('src'): time.sleep(0.1)
            binaries.append(browser.get_blob(el.get_attribute('src')))
        browser.save_images_from_bytes(self.parser.prepare_save_folder(self.parser.current_title), binaries)    
