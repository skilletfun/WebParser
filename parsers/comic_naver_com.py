from parsers.basic_parser import basic_parser
import time
import requests

class comic_naver_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        old_url = ''
        url = self.attrs['url']

        if 'weekday' in url:
            url = url[:url.find('weekday') - 1]

        while True:
            self.attrs['chapter_count'] -= self.attrs['step']

            headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
            response = requests.get(url, headers=headers)

            if 'list?titleId' in response.url or old_url == url: break

            src = response.text
            title, images = self.find_images(src, 'div', 'class', 'wt_viewer')
            title += str(int(url[url.rfind('=') + 1:]))
            images = [img.get('src') for img in images]

            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                old_url = url
                url = url[:url.rfind('=') + 1] + str(int(url[url.rfind('=') + 1:]) + 1)
                self.save_folder = self.true_save_folder
            else: break
        return True