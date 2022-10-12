import os
import asyncio
from typing import Tuple

import aiofiles
import requests
import requests_async
from PyQt5.QtCore import QObject
from bs4 import BeautifulSoup as bs

import config
from utils.logging import log
from utils import file_transform


class basic_parser(QObject):
    def __init__(self) -> None:
        super(basic_parser, self).__init__()
        # Статистика для загрузчика в QML
        self.total_images = 0
        self.total_download_images = 0
        self.current_title = ''

    @log
    async def download(self, url: str, name: str) -> None:
        """ Загружает картинку по ссылке. """
        headers = config.HEADERS
        headers['Host'] = url.replace('http://', '').replace('https://', '').split('/')[0]
        async with self.sem:
            async with requests_async.Session() as session:
                tries = config.DOWNLOAD_TRIES
                status = 0
                img = None

                while (not status == 200) and tries > 0:
                    img = await session.get(url, headers=headers)
                    status = img.status_code
                    tries -= 1
                    await asyncio.sleep(0.5)

                if status == 200:
                    f = await aiofiles.open(os.path.join(self.save_folder, name + '.jpg'), mode="wb")
                    await f.write(await img.read())
                    await f.close()
                    await img.close()
                    self.total_download_images += 1

    @log
    def find_element(self, src: str, tag: str, type: str, value: str) -> str:
        """ Находит указанный элемент в html-разметке. """
        return bs(src, "lxml").find(tag, {type: value})

    @log
    def get_response(self, url: str) -> str:
        """ Посылает запрос и возвращает результат в текстовом виде. """
        return requests.get(url).text

    @log
    def prepare_save_folder(self, title: str) -> str:
        """ Подготавливает (создает) папку для сохранения сканов. """
        title = ''.join(el for el in title if not el in ' .|/\\?*><:"!^;,№')
        folder = orig_folder = os.path.join(config.SAVE_FOLDER, title)
        i = 1
        while True:
            if os.path.exists(folder):
                folder = orig_folder + '_' + str(i)
                i += 1
                continue
            os.mkdir(folder)
            break
        self.save_folder = folder
        return folder

    @log
    def find_images(self, src: str, tag_type: str, ttfs: str, value_of_ttfs: str, tag: str=None) -> Tuple[str, list]:
        """ Находит в разметке ссылки на картинки и возвращает список с картинками и название главы.  """
        soup = bs(src, "lxml")
        title_page = soup.find('title').text
        images = soup.find(tag_type, {ttfs: value_of_ttfs})
        tag = tag if tag else 'img' 
        images = images.find_all(tag)
        return title_page, images

    @log
    def download_images(self, images: list) -> None:
        """ Запускает скачку картинок. """
        asyncio.run(self.async_download_images(images))

    @log
    async def async_download_images(self, images: list) -> None:
        """ Скачка картинок. """
        self.sem = asyncio.Semaphore(config.REQUESTS_LIMIT)
        await asyncio.gather(*[asyncio.create_task(self.download(el[1], str(el[0]))) for el in enumerate(images, 1)])

    @log
    def check_checkboxes(self, title: str) -> None:
        """ Если отмечены опции, то выполнение соответствующих действий. """
        if False:
            file_transform.merge_images(config.SAVE_FOLDER)
        if False:
            file_transform.archivate(config.SAVE_FOLDER, title)

    @log
    def full_download(self, images: list, title: str) -> None:
        """ Базовая полная загрузка. """
        self.current_title = title
        self.total_images = len(images)
        self.total_download_images = 0
        self.prepare_save_folder(title)
        self.download_images(images)
        self.check_checkboxes(title)
