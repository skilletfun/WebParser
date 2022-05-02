from parsers.basic_parser import basic_parser
import time
from bs4 import BeautifulSoup as bs

class mangakakalot_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.attrs['timeout'] = 2

        while True:
            self.attrs['chapter_count'] -= self.attrs['step']
            src = self.get_response(self.attrs['url'])
            title, images = self.find_images(src, 'div', 'class', 'container-chapter-reader')
            images = [img.get('src') for img in images]

            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                soup = bs(src, 'lxml')
                res = soup.find_all('a', {'class': 'back'})[-1]
                if res:
                    self.attrs['url'] = res.get('href')
                    self.save_folder = self.true_save_folder
                else: return True
            else: return True
