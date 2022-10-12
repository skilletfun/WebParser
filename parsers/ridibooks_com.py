from utils.basic_parser import basic_parser
import time

class ridibooks_com(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(user=True)
        old_title = ''
        base_url = 'document.getElementsByClassName(\'pages\')[0]'
        self.browser.execute_script('window.stop();')
        time.sleep(1)
        self.browser.switch_to.new_window('tab')
        self.browser.get(self.attrs['url'])
        self.browser.minimize_window()

        while True:
            # load all images by scroll
            flag = False
            try:
                length = self.browser.execute_script(f'return {base_url}.getElementsByClassName(\'lazy_load\').length;')
            except:
                time.sleep(1)
                continue

            time_for_check = self.config['scroll_delay']
            while not flag:
                for i in range(length):
                    self.browser.execute_script(f'{base_url}.getElementsByClassName(\'lazy_load\')[{i}].scrollIntoView();')
                    time.sleep(time_for_check)
                time_for_check /= 2
                time.sleep(3)
                if length == self.browser.execute_script(f'return {base_url}.getElementsByClassName(\'loaded\').length;'):
                    flag = True
            # end loading

            self.attrs['chapter_count'] -= self.attrs['step']

            title = self.browser.title
            if title == old_title: break

            sort_names = lambda x: int(x.url[x.url.index('__ridi__') + 8 : x.url.index('.jpg?')])
            sort_urls = lambda x: self.attrs['url'][self.attrs['url'].rfind('/'):] + '/webtoon/__ridi__' in x.url

            images_in_bytes = [el.response.body for el in sorted(list(filter(sort_urls, self.browser.requests)), key=sort_names)]

            self.save_images_from_bytes(images_in_bytes, title)
            del self.browser.requests

            if self.attrs['chapter_count'] > 0:
                s_next = "document.getElementsByClassName('next_button')[0].click();"
                self.try_next_chapter(self.browser, s_next, title)
                self.attrs['url'] = self.browser.current_url
            else: break

        self.browser.close()
        self.browser.quit()
        return True
