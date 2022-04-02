from parsers.basic_parser import basic_parser


class comico_kr(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)

        browser = self.init_browser(user=True)

        old_title = ''

        try:
            browser.execute_script('window.stop();')
            browser.switch_to.new_window('tab')
            time.sleep(1)

            browser.get(self.url)
            browser.minimize_window()

            temp_check = -1

            while True:
                time.sleep(5)

                check = browser.execute_script('return document.getElementsByClassName(\'viewer_comic\')[0];')

                if check is None:
                    continue
                elif int(check.get_attribute('childElementCount')) < 1 or int(check.get_attribute('childElementCount')) != temp_check:
                    temp_check = int(check.get_attribute('childElementCount'))
                    continue

                self.chapter_count -= self.step

                title = browser.execute_script('return document.getElementsByClassName(\'tit_comic\')[0].textContent;')
                if title == old_title: break

                self.current_title = title
                self.total_images = int(browser.execute_script("return document.getElementsByClassName('viewer_comic')[0].children.length;"))
                self.total_download_images = 0

                now_downloaded = len(list(filter(lambda x: '?Policy=' in x.url, browser.requests)))

                while now_downloaded < self.total_images:
                    now_downloaded = len(list(filter(lambda x: '?Policy=' in x.url, browser.requests)))
                    self.total_download_images = now_downloaded
                    time.sleep(1)

                time.sleep(3)

                reqs = list(filter(lambda x: '?Policy=' in x.url, browser.requests))
                images_in_bytes = []

                images = browser.execute_script('return document.getElementsByClassName(\'viewer_comic\')[0].getElementsByTagName(\'style\');')
                images = [el.get_attribute('innerHTML') for el in images]
                images_names = [el[el.index('https://') : el.index('\');')] for el in images if '0px' not in el.split()]

                for i in range(self.total_images):
                    for j in range(len(reqs)):
                        if images_names[i] in reqs[j].url:
                            images_in_bytes.append(reqs[j].response.body)
                            reqs.pop(j)
                            break

                self.save_images_from_bytes(images_in_bytes, title)

                if self.chapter_count > 0:
                    s_next = "document.getElementsByClassName('link_next')[0].click();"
                    s_title = "return document.getElementsByClassName('tit_comic')[0].textContent;"
                    self.try_next_chapter(browser, s_next, title, s_title)
                else: break
        except Exception as e:
            print(e)
        finally:
            browser.close()
            browser.quit()
