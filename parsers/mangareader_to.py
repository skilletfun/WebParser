from parsers.basic_parser import basic_parser

class mangareader_to(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        from bs4 import BeautifulSoup as bs
        import time, sys
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("window-size=900,600")

        ex_path = self.get_chromedriver_path()

        browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)

        old_title = ''

        try:
            browser.get(self.url)
            while True:
                self.chapter_count -= self.step
                check = browser.execute_script('return document.getElementsByClassName(\'rtl-row mode-item\')[0];')

                if not check is None:
                    browser.execute_script('document.getElementsByClassName(\'rtl-row mode-item\')[0].click();')

                time.sleep(5)
                html = browser.execute_script(
                    'return document.getElementsByClassName(\'container-reader-chapter\')[0].innerHTML;')

                soup = bs(html, 'lxml')
                title = str(browser.current_url).split('/')[-1]
                if title == old_title: break
                images = [el['data-url'] for el in soup.find_all('div', {'class': 'iv-card'})]

                self.full_download(images, title)

                if self.chapter_count > 0:
                    browser.execute_script('nextChapterVolume();')
                    self.save_folder = self.true_save_folder
                    old_title = title
                else: break
        finally: browser.close()
