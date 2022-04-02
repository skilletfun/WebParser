from parsers.basic_parser import basic_parser


class ridibooks_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        browser = self.init_browser(user=True)

        old_title = ''
        base_url = 'document.getElementsByClassName(\'pages\')[0]'

        try:
            browser.execute_script('window.stop();')
            time.sleep(0.5)
            browser.switch_to.new_window('tab')
            browser.get(self.url)

            while True:
                # load all images by scroll
                flag = False
                try:
                    length = browser.execute_script(f'return {base_url}.getElementsByClassName(\'lazy_load\').length;')
                except:
                    time.sleep(1)
                    continue

                time_for_check = self.config['scroll_delay']
                while not flag:
                    for i in range(length):
                        browser.execute_script(f'{base_url}.getElementsByClassName(\'lazy_load\')[{i}].scrollIntoView();')
                        time.sleep(time_for_check)
                    time_for_check /= 2
                    time.sleep(3)
                    if length == browser.execute_script(f'return {base_url}.getElementsByClassName(\'loaded\').length;'):
                        flag = True
                # end loading

                self.chapter_count -= self.step

                title = browser.title
                if title == old_title: break

                sort_names = lambda x: int(x.url[x.url.index('__ridi__') + 8 : x.url.index('.jpg?')])

                images_in_bytes = [el.response.body for el in sorted(list(filter(lambda x: self.url[self.url.rfind('/'):] + '/webtoon/__ridi__' in x.url, browser.requests)), key=sort_names)]

                self.save_images_from_bytes(images_in_bytes, title)

                if self.chapter_count > 0:
                    s_next = "document.getElementsByClassName('next_button')[0].click();"
                    self.try_next_chapter(browser, s_next, title)
                else: break
        except Exception as e:
            print(e)
        finally:
            browser.close()
            browser.quit()
