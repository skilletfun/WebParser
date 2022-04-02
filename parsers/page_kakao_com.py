from parsers.basic_parser import basic_parser


class page_kakao_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        browser = self.init_browser(user=True)

        browser.minimize_window()

        old_title = ''

        try:
            browser.execute_script('window.stop();')
            browser.switch_to.new_window('tab')
            time.sleep(1)
            browser.get(self.url)

            while True:
                check = browser.execute_script("return document.getElementsByClassName('css-88gyaf')[0];")

                if check is None:
                    time.sleep(1)
                    continue

                self.chapter_count -= self.step

                title = browser.execute_script('return document.getElementsByClassName(\'titleWrap\')[0].children[0].textContent;')
                if title == old_title: break

                images = browser.execute_script(
                    'return document.getElementsByClassName(\'css-88gyaf\')[0].getElementsByTagName(\'img\');')

                images = [el.get_attribute('src') for el in images]

                self.full_download(images, title)

                if self.chapter_count > 0:
                    s_next = "document.getElementsByClassName('linkItem')[3].click();"
                    s_title = "return document.getElementsByClassName('titleWrap')[0].children[0].textContent;"
                    self.try_next_chapter(browser, s_next, title, s_title)
                else: break
        finally:
            browser.close()
            browser.quit()
