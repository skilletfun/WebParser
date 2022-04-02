from parsers.basic_parser import basic_parser


class mangakakalots_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        self.timeout = 2
        self.limit = 10

        while True:
            self.chapter_count -= self.step
            src = self.get_response(self.url)

            title, images = self.find_images(src, 'div', 'id', 'vungdoc')

            images = [img.get('src') for img in images]

            self.full_download(images, title)

            time.sleep(5)

            if self.chapter_count > 0:
                soup = bs(src, 'lxml')
                res = soup.find_all('a', {'class': 'next'})[-1]
                if not res is None:
                    self.url = 'https://ww2.mangakakalots.com/' + res.get('href')
                    self.save_folder = self.true_save_folder
                else:
                    break
            else:
                break
