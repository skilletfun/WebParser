import sys
import time
import base64
from typing import Any, Callable
from os.path import join

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.logging import log
from config import SCROOL_DELAY


class Browser:
    """ Класс для управляения браузером. """
    def __init__(self, full_load: bool=True):
        options = Options()
        options.add_argument("--disable-features=VizDisplayCompositor")
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

    def get(self, url: str) -> str:
        """ Загружает страницу. """
        self.driver.get(url)
        return self.driver.page_source

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
        """ Проверяет, есть ли на странице указанный элемент
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

    def requests(self):
        return self.driver.requests

    def clear_requests(self):
        del self.driver.requests

    def current_url(self):
        return self.driver.current_url

    @log
    def save_images_from_bytes(self, path: str, list_bytes: list) -> None:
        """ Сохраняет картинки из перехваченных байтов. """
        for name, img in zip(range(1, len(list_bytes) + 1), list_bytes):
            with open(join(path, str(name) + '.jpg'), mode="wb") as f:
                f.write(img)
                f.close()
        self.clear_requests()

    @log
    def scroll_page(self, element: str, check: Callable) -> None:
        length = int(self.execute('return ' + element + '.length;'))
        # Первый круг прогрузки
        for i in range(length):
            self.execute(element + f'[{i}].scrollIntoView();')
            time.sleep(SCROOL_DELAY)
        # Финальный круг прогрузки. Будет грузиться, пока не прогрузится все
        for i in range(length):
            self.execute(element + f'[{i}].scrollIntoView();')
            # Если условие не выполнено (элемент не прогружен), то попытаться еще раз
            while check(i):
                time.sleep(SCROOL_DELAY)

    @log
    def get_blob(self, uri):
        result = self.driver.execute_async_script("""
            var uri = arguments[0];
            var callback = arguments[1];
            var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
            var xhr = new XMLHttpRequest();
            xhr.responseType = 'arraybuffer';
            xhr.onload = function(){ callback(toBase64(xhr.response)) };
            xhr.onerror = function(){ callback(xhr.status) };
            xhr.open('GET', uri);
            xhr.send();
            """, uri)
        if type(result) == int :
            raise Exception("Request failed with status %s" % result)
        return base64.b64decode(result)

    def __del__(self):
        self.shutdown()
