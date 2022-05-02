from parsers.basic_parser import basic_parser
import time


class kuaikanmanhua_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(headless=True)

        while True:
            self.attrs['chapter_count'] -= self.attrs['step']
            self.browser.get(self.attrs['url'])
            src = self.browser.page_source
            title, images = self.find_images(src, 'div', 'class', 'imgList')
            images = [img.get('data-src') for img in images if not img.get('data-src') is None]

            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                res = self.find_element(src, 'div', 'class', 'AdjacentChapters').find_all('a')[-1]
                if 'javascript' not in res:
                    self.attrs['url'] = 'https://www.kuaikanmanhua.com' + res.get('href')
                    self.save_folder = self.true_save_folder
                else: break
            else: break

        self.browser.close()
        self.browser.quit()
        return True
