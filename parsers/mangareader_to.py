from parsers.basic_parser import basic_parser
import time
from bs4 import BeautifulSoup as bs


class mangareader_to(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(headless=True)
        old_title = ''
        self.browser.get(self.attrs['url'])

        while True:
            self.attrs['chapter_count'] -= self.attrs['step']
            check = self.browser.execute_script("return document.getElementsByClassName('rtl-row mode-item')[0];")

            if check:
                self.browser.execute_script("document.getElementsByClassName('rtl-row mode-item')[0].click();")

            time.sleep(5)

            html = self.browser.execute_script("return document.getElementsByClassName('container-reader-chapter')[0].innerHTML;")
            soup = bs(html, 'lxml')
            title = str(self.browser.current_url).split('/')[-1]
            if title == old_title: break
            images = [el['data-url'] for el in soup.find_all('div', {'class': 'iv-card'})]

            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                self.browser.execute_script('nextChapterVolume();')
                self.save_folder = self.true_save_folder
                old_title = title
            else: break
        self.browser.close()
        self.browser.quit()
        return True
