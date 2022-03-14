from parsers.basic_parser import basic_parser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import sys


class manga_bilibili_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("window-size=900,600")

        ex_path = self.get_chromedriver_path()

        browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
        browser.get(self.url)

        old_tilte = ''

        while True:
            self.chapter_count -= self.step

            browser.execute_script("document.getElementsByClassName(\"info-hud\")[0].style.display = \"none\";")
            browser.execute_script("document.getElementsByClassName(\"message-box\")[0].style.display = \"none\";")
            browser.execute_script("document.getElementsByClassName(\"manga-reader-ui\")[0].style.display = \"none\";")
            browser.execute_script("document.getElementsByClassName(\"floating-buttons\")[0].style.display = \"none\";")
            browser.execute_script("document.getElementsByClassName(\"ps__rail-y\")[0].style.display = \"none\";")
            browser.execute_script("document.getElementsByClassName(\"ps__thumb-y\")[0].style.display = \"none\";")

            time.sleep(15)

            script = "return document.getElementsByClassName(\"image-list\")[0].getElementsByClassName(\"image-item\").length;"
            count_of_images = int(browser.execute_script(script))

            if not self.redownload_numbers == '':
                numbers = self.redownload_numbers.split()
                numbers = [int(i) - 1 for i in numbers]
                self.timeout = 10
            else:
                numbers = list(range(count_of_images))

            title = browser.execute_script('return document.title;')

            if title == old_tilte: break

            self.save_folder = self.prepare_save_folder(self.save_folder, title)

            for element in numbers:
                width = str(browser.execute_script(f"return document.getElementsByClassName(\"image-list\")[0]"
                                                   f".getElementsByClassName(\"image-item\")[{element}].style.width;"))[:-2]
                height = str(browser.execute_script(f"return document.getElementsByClassName(\"image-list\")[0]"
                                                    f".getElementsByClassName(\"image-item\")[{element}].style.height;"))[:-2]
                browser.set_window_size(width=int(width), height=int(height))
                browser.execute_script(f"document.getElementsByClassName(\"image-item\")[{element}].scrollIntoView();")
                time.sleep(self.timeout)
                browser.save_screenshot(os.path.join(self.save_folder, f'{element + 1}.png'))

            self.check_all_checkboxes()

            if self.chapter_count > 0:
                browser.execute_script('return document.getElementsByClassName(\'pagedown\')[0].click();')
                self.save_folder = self.true_save_folder
                old_tilte = title
            else: break
