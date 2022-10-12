from utils.basic_parser import basic_parser
import time


class bomtoon_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(user=True)
        old_title = ''

        self.browser.switch_to.new_window('tab')
        time.sleep(1)
        self.browser.get(self.attrs['url'])
        self.browser.minimize_window()

        while True:
            total_images = int(self.browser.execute_script("return document.getElementById('bt-data').getAttribute('data-total-page');"))
            images_names = self.browser.execute_script("return document.getElementById('bt-data').getAttribute('data-images');").split(',')
            images_names = [el[el.find('/') : el.find('?')] for el in images_names] # sorted names (parts of urls) of images

            self.attrs['chapter_count'] -= self.attrs['step']

            title = self.browser.title
            if title == old_title: break

            # For animate downloading in GUI
            self.current_title = title
            self.total_images = total_images
            self.total_download_images = 0

            # Loading all images
            now_downloaded = 0
            while now_downloaded < total_images:
                time.sleep(0.5)
                now_downloaded = len(list(filter(lambda x: '?Policy=' in x.url, self.browser.requests)))
                if now_downloaded != self.total_download_images:
                    self.browser.execute_script('window.scrollBy(0,1500);')
                self.total_download_images = now_downloaded
            time.sleep(3)

            # Sort
            reqs = list(filter(lambda x: '?Policy=' in x.url, self.browser.requests))
            images_in_bytes = []
            for i in range(total_images):
                for j in range(len(reqs)):
                    if images_names[i] in reqs[j].url:
                        images_in_bytes.append(reqs[j].response.body)
                        i += 1
                        reqs.pop(j)
                        break

            self.save_images_from_bytes(images_in_bytes, title)
            del self.browser.requests

            if self.attrs['chapter_count'] > 0:
                s_next = "document.getElementById('bt-btn-next').click();"
                self.try_next_chapter(self.browser, s_next, title)
            else: break

        self.browser.close()
        self.browser.quit()
        return True