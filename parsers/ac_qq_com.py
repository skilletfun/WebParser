from parsers.basic_parser import basic_parser


class ac_qq_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)

        browser = self.init_browser(headless=True)

        try:
            while True:
                self.chapter_count -= self.step
                browser.get(self.url)

                time.sleep(2)

                script = "document.getElementById('comicContain').getElementsByTagName('img')"

                l = int(browser.execute_script('return ' + script + '.length;'))
                images = []

                for i in range (l):
                    browser.execute_script(script + f'[{i}].scrollIntoView();')
                    time.sleep(0.5)

                for i in range (l):
                    browser.execute_script(script + f'[{i}].scrollIntoView();')
                    while browser.execute_script('return ' + script + f'[{i}].src;').endswith('pixel.gif'):
                        continue
                    images.append(browser.execute_script('return ' + script + f'[{i}].src;'))

                title = browser.title
                images = images[:1] + images[2:]

                self.full_download(images, title)

                if self.chapter_count > 0:
                    self.url = browser.execute_script("return document.getElementById('nextChapter').href;")
                    self.save_folder = self.true_save_folder
                else:
                    break
        finally:
            browser.close()
            browser.quit()
