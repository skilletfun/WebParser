import time

from selenium.webdriver.common.by import By

from utils.basic_parser import basic_parser
#https://mechacomic.jp/viewer/index.html?colophon=https%3A%2F%2Fmechacomic.jp%2Ffree_chapters%2F2086938%2Fcolophon%3Fback_path%3D%252Fbooks%252F157299%26v%3D2%26vertical%3Don&colophon_size=320_340&contents_vertical=https%3A%2F%2Fc.cnt.mechacomic.jp%2Fviewer%2Fdata%2F2141%2Fakujonanonimama_001_a_wt%2Fcontents_vertical.json&cryptokey=https%3A%2F%2Fmechacomic.jp%2Fviewer_cryptokey%2Ffree_chapter%2F2086938&directory=https%3A%2F%2Fc.cnt.mechacomic.jp%2Fviewer%2Fdata%2F2141%2Fakujonanonimama_001_a_wt%2F&ga_params=%7B%22mbr%22%3A%220%22%2C%22lgn%22%3A%220%22%2C%22bid%22%3A157299%2C%22cno%22%3A1%7D&help=https%3A%2F%2Fmechacomic.jp%2Finfo%2Fviewer_help2&icon=https%3A%2F%2Fc.mechacomic.jp%2Fimages%2Fparts%2Fviewer_ui_icons.png&logo=https%3A%2F%2Fc.mechacomic.jp%2Fimages%2Fparts%2Fviewer_new_logo_white.png&margin=0&popup=https%3A%2F%2Fmechacomic.jp%2Ffree_chapters%2F2086938%2Fcolophon%3Fback_path%3D%252Fbooks%252F157299%26v%3D2%26vertical%3Don&popup_size=320_340&return_to=https%3A%2F%2Fmechacomic.jp%2Fbooks%2F157299&ver=b9581a6959311d178c76dac57643f8d5&viewer=vertical

class mechacomic_jp(basic_parser):
    @basic_parser.logging
    def parse(self, attrs):
        self.update_vars(attrs)
        self.browser = self.init_browser(user=True)
        old_title = ''
        self.browser.switch_to.new_window('tab')
        time.sleep(0.5)
        self.browser.get(self.attrs['url'])
        time.sleep(10)

        try:
            while True:
                total_img_script = "return document.getElementsByClassName('VerticalViewer__WebtoonPageList-sc-10lu0rw-2')[0].children.length;"
                total_images = int(self.browser.execute_script(total_img_script))

                self.attrs['chapter_count'] -= self.attrs['step']

                title = self.browser.title
                if title == old_title: break

                # For animate downloading in GUI
                self.current_title = title
                self.total_images = total_images
                self.total_download_images = 0

                try:
                    if self.browser.find_element(By.CLASS_NAME, 'ContinueDialog__CancelButton-sc-1yg6q2m-1'):
                        self.browser.execute_script("document.getElementsByClassName('ContinueDialog__CancelButton-sc-1yg6q2m-1')[0].click();")
                        time.sleep(1)
                except:
                    pass

                # Loading all images
                now_downloaded = 0
                script = "return document.getElementsByClassName('WebtoonPageContainer__Image-cry93q-1')"
                images = self.browser.execute_script(script+';')

                for el in enumerate(images[:15]):
                    while True:
                        self.browser.execute_script(script + f'[{el[0]}].scrollIntoView();')
                        if el[1].get_attribute('src'):

                            now_downloaded += 1
                            break
                        time.sleep(0.5)

                    self.total_download_images = now_downloaded

                print(*self.browser.requests, sep='\n\n')

                # Sort
                reqs = list(filter(lambda x: x.url.startswith('blob:https://mechacomic.jp'), self.browser.requests))
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
        except Exception as e:
            raise e
        finally:
            self.browser.close()
            self.browser.quit()
            return True