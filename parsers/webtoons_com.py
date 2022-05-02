from parsers.basic_parser import basic_parser


class webtoons_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)

        while True:
            self.attrs['chapter_count'] -= self.attrs['step']
            src = self.get_response(self.attrs['url'])
            title, images = self.find_images(src, 'div', 'id', '_imageList')
            images = [img.get('data-url') for img in images]
            
            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                res = self.find_element(src, 'a', 'class', '_nextEpisode')
                if not res is None:
                    self.attrs['url'] = res.get('href')
                    self.save_folder = self.true_save_folder
                else: break
            else: break
        return True
