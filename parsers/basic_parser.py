import requests
import os
from bs4 import BeautifulSoup as bs

import asyncio
import aiohttp
import aiofiles

from PyQt5.QtCore import QObject, pyqtSignal

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
                print('Exception:', e)
                connector = await aiohttp.TCPConnector(force_close=True)
                session = await aiohttp.ClientSession(connector=connector)
                await asyncio.sleep(1)

        if status == 200:
            f = await aiofiles.open(os.path.join(save_folder, name + '.jpg'), mode="wb")
            await f.write(await img.read())
            await f.close()
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


    def download_images(self, images, save_folder, url, timeout, _headers=None, name_of_files=''):
        """ Download images by urls. Start async function. """
    
        asyncio.run(self.t_download_images(images, save_folder, url, timeout, _headers, name_of_files))


    async def t_download_images(self, images, save_folder, url, timeout, _headers=None, name_of_files=''):
        """ Download images by urls. """
    
        if _headers is None:
            _headers = {
                "Accept": "image/webp,*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                'Host': '',
                "DNT": "1",
                "Referer": url,
                "Sec-GPC": "1",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
            }

        if name_of_files == '':
            name_of_files = [el + 1 for el in range(len(images))]
        else:
            name_of_files = name_of_files.split()

        i = 0
        tasks = []

        sem = asyncio.Semaphore(self.config['semaphore_limit'] + int(timeout) * 1000)
        async with sem:
            connector = aiohttp.TCPConnector(force_close=True, limit=self.config['requests_limit'])
            async with aiohttp.ClientSession(connector=connector) as session:
                for img_url in images:
                    temp_url = img_url

                    if 'Host' in _headers:
                        _headers['Host'] = temp_url.replace('http://', '').replace('https://', '').split('/')[0]

                    task = asyncio.create_task(
                        self.download(session, img_url, _headers, str(name_of_files[i]), save_folder))
                    tasks.append(task)
                    i += 1
                await asyncio.gather(*tasks)


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

        self.save_folder = self.prepare_save_folder(title)
        self.download_images(images, self.save_folder, self.url, self.timeout, name_of_files=self.redownload_numbers)
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
    
        import sys

        if not sys.platform.startswith("linux"):
            ex_path = 'chromedriver.exe'
        else:
            ex_path = 'chromedriver'
        return ex_path
