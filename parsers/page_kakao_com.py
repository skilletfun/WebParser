from parsers.basic_parser import basic_parser
import time


class page_kakao_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(user=True, full_load=False)
        old_title = ''
        self.browser.switch_to.new_window('tab')
        time.sleep(1)
        self.browser.get(self.attrs['url'])
        self.browser.minimize_window()

        while True:
            check = self.browser.execute_script("return document.getElementsByClassName('css-88gyaf')[0];")

            if check is None:
                time.sleep(1)
                continue
            else:
                self.browser.execute_script('window.stop();')

            self.attrs['chapter_count'] -= self.attrs['step']

            title = self.browser.execute_script("return document.getElementsByClassName('titleWrap')[0].children[0].textContent;")
            if title == old_title: break

            images = self.browser.execute_script(
                "return document.getElementsByClassName('css-88gyaf')[0].getElementsByTagName('img');")

            images = [el.get_attribute('src') for el in images]
            self.full_download(images, title)

            if self.attrs['chapter_count'] > 0:
                s_next = "document.getElementsByClassName('linkItem')[3].click();"
                s_title = "return document.getElementsByClassName('titleWrap')[0].children[0].textContent;"
                self.try_next_chapter(self.browser, s_next, title, s_title)
            else: break

        self.browser.close()
        self.browser.quit()
        return True
