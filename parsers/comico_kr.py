from parsers.basic_parser import basic_parser
import time


class comico_kr(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(user=True)
        old_title = ''

        self.browser.switch_to.new_window('tab')
        time.sleep(1)
        self.browser.get(self.attrs['url'])
        self.browser.minimize_window()

        temp_check = -1

        while True:
            time.sleep(5)
            check = self.browser.execute_script('return document.getElementsByClassName(\'viewer_comic\')[0];')

            if check is None:
                continue
            elif int(check.get_attribute('childElementCount')) < 1 or int(check.get_attribute('childElementCount')) != temp_check:
                temp_check = int(check.get_attribute('childElementCount'))
                continue

            self.attrs['chapter_count'] -= self.attrs['step']

            title = self.browser.execute_script("return document.getElementsByClassName('tit_comic')[0].textContent;")
            if title == old_title: break

            self.current_title = title
            self.total_images = int(self.browser.execute_script("return document.getElementsByClassName('viewer_comic')[0].children.length;"))
            self.total_download_images = 0

            now_downloaded = len(list(filter(lambda x: '?Policy=' in x.url, self.browser.requests)))

            while now_downloaded < self.total_images:
                now_downloaded = len(set(filter(lambda x: '?Policy=' in x.url, self.browser.requests)))
                self.total_download_images = now_downloaded
                time.sleep(1)

            time.sleep(3)

            reqs = set(filter(lambda x: '?Policy=' in x.url, self.browser.requests))
            images_in_bytes = []

            images = self.browser.execute_script("return document.getElementsByClassName('viewer_comic')[0].getElementsByTagName('style');")
            images = [el.get_attribute('innerHTML') for el in images]
            images_names = [el[el.index('https://') : el.index('\');')] for el in images if '0px' not in el.split()]

            reqs = list(reqs)
            for i in range(self.total_images):
                for j in range(len(reqs)):
                    if images_names[i] in reqs[j].url:
                        images_in_bytes.append(reqs[j].response.body)
                        reqs.pop(j)
                        break

            self.save_images_from_bytes(images_in_bytes, title)
            del self.browser.requests

            if self.attrs['chapter_count'] > 0:
                s_next = "document.getElementsByClassName('link_next')[0].click();"
                s_title = "return document.getElementsByClassName('tit_comic')[0].textContent;"
                self.try_next_chapter(self.browser, s_next, title, s_title)
            else: break

        self.browser.close()
        self.browser.quit()
        return True
