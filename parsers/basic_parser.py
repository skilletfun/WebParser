import time
import sys
import requests
import os
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup as bs
from PyQt5.QtCore import QObject, pyqtSignal
from parsers.basic_parser import basic_parser
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class basic_parser(QObject):
    url = None
    timeout = None
    save_folder = None
    true_save_folder = None
    redownload_numbers = None
    do_archive = None
    do_merge = None
    chapter_count = None
    step = None
    
    config = None

    # Statistic for QML
    total_images = 0
    total_download_images = 0
    current_title = ''


    def __init__(self, config):
        super(basic_parser, self).__init__()
        self.config = config
        
        if not config['remember_save_folder']: self.save_folder = ''
        else: self.save_folder = config['save_folder']


    def init_browser(self, *, user=False, headless=False, disable_images=False):
        """ Init webdriver. Base for many parsers. """
        options = Options()
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--disable-extensions')

        if user:
            options.add_argument("--user-data-dir=" + self.config['path_to_browser'])

        if sys.platform.startswith('linux'):
            options.add_argument('--password-store=gnome')

        if headless:
            options.add_argument("--headless")

        if disable_images:
            options.add_argument('--blink-settings=imagesEnabled=false')

        ex_path = self.get_chromedriver_path()
        return webdriver.Chrome(chrome_options=options, executable_path=ex_path)


    def update_vars(self, attrs):
        """ Update values of self vars from attrs. """
    
        self.url = attrs['url']
        self.timeout = attrs['timeout']
        self.true_save_folder = self.save_folder
        self.redownload_numbers = attrs['redownload_numbers']
        self.do_archive = attrs['do_archive']
        self.do_merge = attrs['do_merge']
        self.chapter_count = attrs['chapter_count']

        if not self.url.startswith('http'):
            self.url = 'https://' + self.url

        if self.chapter_count != '*':
            self.chapter_count = int(self.chapter_count)
            self.step = 1
        else:
            self.step = 0
            self.chapter_count = 1


    async def download(self, session, url, _headers, name, save_folder):
        """ Download function. Declare single because of async. """
    
        tries = self.config['download_tries']
        status = 0

        while (not status == 200) and tries > 0:
            try:
                img = await session.get(url, headers=_headers)
                status = img.status
                tries -= 1
            except Exception as e:
                print(e)

        if status == 200:
            f = await aiofiles.open(os.path.join(save_folder, name + '.jpg'), mode="wb")
            await f.write(await img.read())
            await f.close()
            img.close()
            self.total_download_images += 1


    def find_element(self, src, tag, type, value):
        """ Find element in html-page. """
    
        soup = bs(src, "lxml")
        res = soup.find(tag, {type: value})
        return res


    def get_response(self, url, headers=None):
        """ Get response and return text. """
    
        if headers is None:
            headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
        response = requests.get(url, headers=headers)
        src = response.text
        return src


    def prepare_save_folder(self, title):
        """ Prepare save folder (create if doesn't exist). """
    
        t_title = ''
        for el in title:
            if not el in ' .|/\\?*><:"!^;,№':
                t_title += el

        save_folder = os.path.join(self.save_folder, t_title)

        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        return save_folder


    def find_images(self, src, tag_type, tag_type_for_search, value_of_ttfs, custom_tag=None):
        """ Parse html and find urls. """
    
        soup = bs(src, "lxml")
        title_page = soup.find('title').text

        images = soup.find(tag_type, {tag_type_for_search: value_of_ttfs})

        if custom_tag is None:
            tag = 'img'
        else:
            tag = custom_tag

        images = images.find_all(tag)

        return title_page, images


    def rebuild_redownload_images(self, numbers, images):
        """ Rebuild array with urls. """
    
        numbers = numbers.split()
        numbers = [int(i) - 1 for i in numbers]

        return [images[i] for i in numbers]


    def download_images(self, images, name_of_files, _headers=None, start_counter=0):
        """ Download images by urls. Start async function. """

        asyncio.run(self.t_download_images(images, name_of_files, _headers, start_counter=start_counter))


    async def t_download_images(self, images, name_of_files, _headers=None, start_counter=0):
        """ Download images by urls. """

        if _headers is None:
            _headers = {
                "Accept": "image/webp,*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                'Host': '',
                "DNT": "1",
                "Referer": self.url,
                "Sec-GPC": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
            }

        i = start_counter
        tasks = []

        sem = asyncio.Semaphore(self.config['semaphore_limit'] + int(self.timeout) * 1000)
        async with sem:
            connector = aiohttp.TCPConnector(force_close=True)
            async with aiohttp.ClientSession(connector=connector) as session:
                for img_url in images:
                    temp_url = img_url

                    if 'Host' in _headers:
                        _headers['Host'] = temp_url.replace('http://', '').replace('https://', '').split('/')[0]

                    task = asyncio.create_task(
                        self.download(session, img_url, _headers, str(name_of_files[i]), self.save_folder))
                    tasks.append(task)
                    i += 1

                await asyncio.gather(*tasks)
            await session.close()


    def check_all_checkboxes(self, title):
        """ Check checkboxes. """
    
        if self.do_merge:
            self.merge_images()

        if self.do_archive:
            self.archivate(title)


    def full_download(self, images, title):
        """ Main function. Start full download. """
    
        self.current_title = title
        self.total_images = len(images)
        self.total_download_images = 0

        if self.redownload_numbers != '':
            images = self.rebuild_redownload_images(self.redownload_numbers, images)
            name_of_files = self.redownload_numbers.split()
        else:
            name_of_files = range(1, len(images)+1)

        self.save_folder = self.prepare_save_folder(title)

        step = self.config['requests_limit']
        for i in range(0, len(images), step):
            try:
                imgs = images[i : i + step]
                self.download_images(imgs, name_of_files, start_counter=i)
            except Exception as e:
                print(e)

        self.check_all_checkboxes(title)


    def archivate(self, title):
        """ Archive images to zip-file. """
    
        import patoolib
        from os.path import split, join

        save_folder = split(self.save_folder)[0]
        t_name = ''

        for el in title:
            if not el in ' .|/\\?*><:"!^;,№':
                t_name += el

        patoolib.create_archive(join(save_folder, t_name + '.zip'), [self.save_folder])

   
    def merge_images(self):
        """ Merge images into one PNG. """
    
        from PIL import Image

        name = os.path.split(self.save_folder)[-1]
        t_name = ''

        for el in name:
            if not el in ' .|/\\?*><:"!^;,№':
                t_name += el

        dir_imgs = os.listdir(self.save_folder)
        suffix = dir_imgs[0].split('.')[-1]
        total = len(dir_imgs)

        height = 0

        imgs = []

        for i in range(1, total + 1):
            img = Image.open(os.path.join(self.save_folder, str(i) + '.' + suffix))
            imgs.append(img)
            height += img.height

        width = imgs[0].width

        save_folder = os.path.abspath(os.path.join(self.save_folder, os.pardir))

        file_name = os.path.join(save_folder, t_name + '_MERGED.png')
        res_img = Image.new('RGB', (width, height), 'white')

        t_height = 0
        for img in imgs:
            res_img.paste(img, (0, t_height))
            t_height += img.height
            img.close()

        res_img.save(file_name, quality=95)
        res_img.close()


    def get_chromedriver_path(self):
        """ Return path to chromedriver. """

        if not sys.platform.startswith("linux"):
            ex_path = 'chromedriver.exe'
        else:
            ex_path = 'chromedriver'
        return ex_path


    def save_images_from_bytes(self, list_bytes, title, names=None):
        """ Save images from bytes (from browser's requests). """
        self.current_title = title
        self.total_images = len(list_bytes)
        self.total_download_images = 0

        if names is None:
            names = range(1, len(list_bytes) + 1)

        self.save_folder = self.prepare_save_folder(title)

        for name, img in zip(names, list_bytes):
            with open(os.path.join(self.save_folder, str(name) + '.jpg'), mode="wb") as f:
                f.write(img)
                f.close()
                self.total_download_images += 1


    def try_next_chapter(self, browser, script_next_chapter, title, script_title=None):
        """ Check existing next chapters if should download it. """
        try:
            old_title = title
            browser.execute_script(script_next_chapter)
            self.save_folder = self.true_save_folder
            max_wait = 10

            while title == old_title and max_wait > 0:
                if not script_title:
                    title = browser.execute_script(script_title)
                else:
                    title = browser.title

                max_wait -= 1
                time.sleep(1)
        except Exception as e:
            print(e)
