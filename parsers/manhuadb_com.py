from utils.basic_parser import basic_parser
import time
from bs4 import BeautifulSoup as bs
import requests


class manhuadb_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        true_url = self.attrs['url']
        soup = self.download_func(self.attrs['url'])
        self.attrs['chapter_count'] -= 1

        while self.attrs['chapter_count'] > 0:
            self.attrs['chapter_count'] -= self.attrs['step']
            chapters_urls = soup.find('ol', {'class': 'links-of-books'}).find_all('a')
            length = len(chapters_urls)

            for i in range(length):
                if chapters_urls[i].get('href') in true_url and i+1 < length:
                    chapters_urls = ['https://www.manhuadb.com' + el.get('href') for el in chapters_urls[i + 1:]]
                    for url in chapters_urls:
                        self.download_func(url)

    def download_func(self, url):
        images = []
        tries = 5

        headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}

        if not url[:-5].endswith('_p1'):
            url = url[:-5] + '_p1.html'

        response = requests.get(url, headers=headers)
        soup = bs(response.text, "lxml")
        title = soup.find('title').text

        while tries > 0:
            response = requests.get(url, headers=headers)
            if response.ok:
                src = response.text
                soup = bs(src, "lxml")
                img = soup.find('img', {'class': 'show-pic'})

                if img != None:
                    images.append(img.get('src'))
                    url = url[:url.rfind('_') + 2] + str(int(url[url.rfind('_') + 2: -5]) + 1) + '.html'
                    tries = 3
                else:
                    break
            else:
                tries -= 1

        self.full_download(images, title)
        return soup
