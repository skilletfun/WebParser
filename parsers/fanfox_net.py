from parsers.basic_parser import basic_parser


class fanfox_net(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        browser = self.init_browser(headless=True)

        try:
            while self.url != 'https://fanfox.net':
                self.chapter_count -= self.step
                images = []
                browser.get(self.url)

                time.sleep(5)

                image = browser.find_element_by_xpath('/html/body/div[7]/img')
                n = int(browser.execute_script('return imagecount'))

                title = browser.execute_script('return document.title')

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

                if self.chapter_count > 0:
                    self.url = 'https://fanfox.net' + browser.execute_script('return nextchapterurl')
                    self.save_folder = self.true_save_folder
                else: break
        finally: browser.close()
