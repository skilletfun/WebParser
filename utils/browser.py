import sys
import time
from typing import Any
from os.path import join

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC

from utils.logging import log


class Browser:
    """ Предоставляет доступ к браузеру. """
    def __init__(self, full_load: bool=True):
        options = Options()
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--disable-extensions')

        if sys.platform.startswith('linux'):
            options.add_argument('--password-store=gnome')

        if not full_load:
            capa = DesiredCapabilities.CHROME
            capa["pageLoadStrategy"] = "none"
            self.driver = webdriver.Chrome(options=options, desired_capabilities=capa)
        else:
            self.driver = webdriver.Chrome(options=options)

        self.CHECK_DICT = {
            By.ID: 'return document.getElementById',
            By.CLASS_NAME: 'return document.getElementsByClassName',
            By.TAG_NAME: 'return document.getElementsByTagName',
        }
        self.driver.switch_to.new_window('tab')

    def get(self, url: str) -> None:
        """ Загружает страницу. """
        self.driver.get(url)

    def go_to_new_tab(self) -> None:
        """ Открывает новую пустую вкладку. """
        self.driver.switch_to.new_window('tab')

    def minimize(self) -> None:
        """ Сворачивает браузер. """
        self.driver.minimize_window()

    def execute(self, script: str, tries: int=5, sleep: float=0.5) -> Any:
        """ Выполняет js-скрипт в браузере
        :param script: скрипт
        :param tries: количество попыток
        :param sleep: время ожидания перед новой попыткой
        :return: результат выполнения
        """
        while tries > 0:
            try:
                return self.driver.execute_script(script)
            except:
                time.sleep(sleep)
                tries -= 1
        return False

    def check_element(self, by: By, value: str, by_driver: bool=False) -> bool:
        """ Проверяет, есть ли на странице элемент
        :param by: как искать элемент [By.CLASS_NAME, By.ID, By.TAG_NAME]
        :param value: значение для поиска
        :param by_driver: искать через метод selenium или через script js
        :return: True / None
        """
        try:
            if by_driver:
                return self.driver.find_element(by, value)
            else:
                return self.driver.execute_script(self.CHECK_DICT[by] + f'("{value}");')
        except:
            return False

    def wait_element(self, by: By, value: str, max_wait: int=10, by_driver: bool=False) -> bool:
        """ Ждет, пока на странице не появится указанный элемент
        :param by: как искать элемент [By.CLASS_NAME, By.ID, By.TAG_NAME]
        :param value: значение элемента, который ожидается
        :param max_wait: сколько секунд ждать
        :param by_driver: искать через метод selenium или через script js
        :return: True / None
        """
        while True:
            if self.check_element(by, value, by_driver):
                time.sleep(0.5)
                return True
            else:
                max_wait -= 0.2
                if max_wait < 0:
                    return False
                time.sleep(0.2)

    def get_source(self) -> str:
        return self.driver.page_source

    def send_keys_to(self, by: By, key: str, value: str) -> None:
        """ Посылает элементу на странице указанное значение.
        :param by: как искать элемент [By.CLASS_NAME, By.ID, By.TAG_NAME]
        :param key: значение элемента, которому шлется value
        :param value: посылаемое значение
        """
        self.driver.find_element(by, key).send_keys(value)

    def shutdown(self) -> None:
        """ Закрывает вкладку и выключает браузер (chromedriver). """
        self.driver.close()
        self.driver.quit()

    def title(self):
        return self.driver.title

    @log
    def save_images_from_bytes(self, path: str, list_bytes: list, title: str) -> None:
        """ Сохраняет картинки, перехватывая байты из запросов. """
        # self.current_title = title
        # self.total_images = len(list_bytes)
        # self.total_download_images = 0
        names = range(1, len(list_bytes) + 1)
        # self.prepare_save_folder()

        for name, img in zip(names, list_bytes):
            with open(join(path, str(name) + '.jpg'), mode="wb") as f:
                f.write(img)
                f.close()
                # self.total_download_images += 1