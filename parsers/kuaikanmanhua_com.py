from parsers.basic_parser import basic_parser


class kuaikanmanhua_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        browser = self.init_browser(headless=True)

        try:
            while True:
                self.chapter_count -= self.step
                browser.get(self.url)
                src = browser.page_source

                title, images = self.find_images(src, 'div', 'class', 'imgList')

                images = [img.get('data-src') for img in images if not img.get('data-src') is None]

                self.full_download(images, title)

                if self.chapter_count > 0:
                    res = self.find_element(src, 'div', 'class', 'AdjacentChapters').find_all('a')[-1]
                    if 'javascript' not in res:
                        self.url = 'https://www.kuaikanmanhua.com' + res.get('href')
                        self.save_folder = self.true_save_folder
                    else:
                        break
                else:
                    break
        finally:
            browser.close()
            browser.quit()
