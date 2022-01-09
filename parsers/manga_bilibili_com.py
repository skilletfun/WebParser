import time
import os
import sys
from parsers.basic_functions import archivate, prepare_save_folder
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("window-size=900,600")

    if not sys.platform.startswith("linux"):
        ex_path = 'chromedriver.exe'
    else:
        ex_path = 'chromedriver'

    browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
    browser.get(url)

    true_save_folder = save_folder
    old_tilte = ''

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1

    while True:
        chapter_count -= step
        browser.execute_script("document.getElementsByClassName(\"info-hud\")[0].style.display = \"none\";")
        browser.execute_script("document.getElementsByClassName(\"message-box\")[0].style.display = \"none\";")
        browser.execute_script("document.getElementsByClassName(\"manga-reader-ui\")[0].style.display = \"none\";")
        browser.execute_script("document.getElementsByClassName(\"floating-buttons\")[0].style.display = \"none\";")
        browser.execute_script("document.getElementsByClassName(\"ps__rail-y\")[0].style.display = \"none\";")
        browser.execute_script("document.getElementsByClassName(\"ps__thumb-y\")[0].style.display = \"none\";")

        time.sleep(15)

        script = "return document.getElementsByClassName(\"image-list\")[0].getElementsByClassName(\"image-item\").length;"
        count_of_images = int(browser.execute_script(script))

        if not redownload_numbers == '':
            numbers = redownload_numbers.split()
            numbers = [int(i) - 1 for i in numbers]
            timeout = 10
        else:
            numbers = list(range(count_of_images))

        title = browser.execute_script('return document.title;')

        if title == old_tilte: break

        save_folder = prepare_save_folder(save_folder, title)

        for element in numbers:
            width = str(browser.execute_script(f"return document.getElementsByClassName(\"image-list\")[0]"
                                               f".getElementsByClassName(\"image-item\")[{element}].style.width;"))[:-2]
            height = str(browser.execute_script(f"return document.getElementsByClassName(\"image-list\")[0]"
                                                f".getElementsByClassName(\"image-item\")[{element}].style.height;"))[:-2]
            browser.set_window_size(width=int(width), height=int(height))
            browser.execute_script(f"document.getElementsByClassName(\"image-item\")[{element}].scrollIntoView();")
            time.sleep(timeout)
            browser.save_screenshot(os.path.join(save_folder, f'{element + 1}.png'))

        if do_archive:
            archivate(save_folder)

        if chapter_count > 0:
            browser.execute_script('return document.getElementsByClassName(\'pagedown\')[0].click();')
            save_folder = true_save_folder
            old_tilte = title
        else: break
