from utils.basic_parser import basic_parser


class webmota_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)

        while True:
            self.attrs['chapter_count'] -= self.attrs['step']
            src = self.get_response(self.attrs['url'])
            title, images = self.find_images(src, 'section', 'class', 'comic-contain', custom_tag='amp-img')
            images = [img.get('src') for img in images]

            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                res = self.find_element(src, 'div', 'class', 'bottom-bar-tool').find_all('a')[3]
                self.attrs['url'] = res.get('href')
                if self.attrs['url']:
                    self.attrs['url'] = res.get('href')
                    self.save_folder = self.true_save_folder
                else: break
            else: break
        return True