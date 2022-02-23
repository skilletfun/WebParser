from parsers.basic_parser import basic_parser

class page_kakao_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)

        print('Chapter_count in start:', self.chapter_count)

        import time, sys
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--user-data-dir=" + self.config['path_to_browser'])

        ex_path = self.get_chromedriver_path()

        browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
        browser.minimize_window()

        old_title = ''

        try:
            browser.execute_script('window.stop();')
            time.sleep(1)
            browser.get(self.url)

            while True:
                check = browser.execute_script('return document.getElementsByClassName(\'css-88gyaf\')[0];')

                if check is None:
                    time.sleep(1)
                    continue

                self.chapter_count -= self.step

                title = browser.execute_script('return document.getElementsByClassName(\'titleWrap\')[0].children[0].textContent;')
                if title == old_title: break

                images = browser.execute_script(
                    'return document.getElementsByClassName(\'css-88gyaf\')[0].getElementsByTagName(\'img\');')

                images = [el.get_attribute('src') for el in images]

                self.full_download(images, title)

                if self.chapter_count > 0:
                    try:
                        old_title = title
                        browser.execute_script('document.getElementsByClassName(\'linkItem\')[3].click();')
                        self.save_folder = self.true_save_folder
                        max_wait = 10

                        while title == old_title and max_wait > 0:
                            title = browser.execute_script('return document.getElementsByClassName(\'titleWrap\')[0].children[0].textContent;')
                            max_wait -= 1
                            time.sleep(1)
                    finally: pass
                else: break
        finally:
            browser.close()
            browser.quit()
