from parsers.basic_parser import basic_parser


class bomtoon_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        self.init_browser(user=True)
        old_title = ''

        try:
            browser.execute_script('window.stop();')
            browser.switch_to.new_window('tab')
            browser.get(self.url)
            browser.minimize_window()

            while True:
                total_images = int(browser.execute_script("return document.getElementById('bt-data').getAttribute('data-total-page');"))
                images_names = browser.execute_script("return document.getElementById('bt-data').getAttribute('data-images');").split(',')

                images_names = [el[el.find('/') : el.find('?')] for el in images_names] # sorted names (parts of urls) of images

                self.chapter_count -= self.step

                title = browser.title
                if title == old_title: break

                # For animate downloading in GUI
                self.current_title = title
                self.total_images = total_images
                self.total_download_images = 0

                # Loading all images
                now_downloaded = 0
                while now_downloaded < total_images:
                    time.sleep(1)
                    now_downloaded = len(list(filter(lambda x: '?Policy=' in x.url, browser.requests)))
                    self.total_download_images = now_downloaded

                time.sleep(3)

                # Sort
                reqs = list(filter(lambda x: '?Policy=' in x.url, browser.requests))
                images_in_bytes = []

                for i in range(total_images):
                    for j in range(len(reqs)):
                        if images_names[i] in reqs[j].url:
                            images_in_bytes.append(reqs[j].response.body)
                            i += 1
                            reqs.pop(j)
                            break

                self.save_images_from_bytes(images_in_bytes, title)

                if self.chapter_count > 0:
                    s_next = "document.getElementById('bt-btn-next').click();"
                    self.try_next_chapter(browser, s_next, title)
                else: break
        except Exception as e:
            print(e)
        finally:
            browser.close()
            browser.quit()
