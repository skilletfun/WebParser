from parsers.basic_parser import basic_parser
import time


class ac_qq_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(headless=True)

        while True:
            self.attrs['chapter_count'] -= self.attrs['step']
            self.browser.switch_to.new_window('tab')
            time.sleep(1)
            self.browser.get(self.attrs['url'])
            time.sleep(2)
            script = "document.getElementById('comicContain').getElementsByTagName('img')"

            length = int(self.browser.execute_script('return ' + script + '.length;'))
            images = []
            for i in range(length):
                self.browser.execute_script(script + f'[{i}].scrollIntoView();')
                time.sleep(0.5)

            for i in range(length):
                self.browser.execute_script(script + f'[{i}].scrollIntoView();')
                while self.browser.execute_script('return ' + script + f'[{i}].src;').endswith('pixel.gif'):
                    continue
                images.append(self.browser.execute_script('return ' + script + f'[{i}].src;'))

            title = self.browser.title
            images = images[:1] + images[2:]

            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                self.attrs['url'] = self.browser.execute_script("return document.getElementById('nextChapter').href;")
                self.save_folder = self.true_save_folder
            else:
                break
        self.browser.close()
        self.browser.quit()
        return True