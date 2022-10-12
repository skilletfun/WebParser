from utils.basic_parser import basic_parser
import time

class fanfox_net(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(headless=True)

        while self.attrs['url'] != 'https://fanfox.net':
            self.attrs['chapter_count'] -= self.attrs['step']
            images = []
            self.browser.get(self.attrs['url'])

            time.sleep(5)

            image = self.browser.find_element_by_xpath('/html/body/div[7]/img')
            n = int(self.browser.execute_script('return imagecount'))
            title = self.browser.execute_script('return document.title')
            url_img = image.get_attribute('src')
            url = url_img.split('?')[0]

            if url[-9] == '/':
                left_url = url[:-7]
                num = '000'
            else:
                pos = url.rfind('_') + 1
                left_url = url[:pos]
                num = str(url[pos:-4])

            for _ in range(n + 1):
                if len(num) < 3:
                    num = (3 - len(num)) * '0' + num

                images.append(left_url + num + '.jpg')
                num = str(int(num) + 1)

            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                self.attrs['url'] = 'https://fanfox.net' + self.browser.execute_script('return nextchapterurl')
                self.save_folder = self.true_save_folder
            else: break
        self.browser.close()
        self.browser.quit()
        return True
