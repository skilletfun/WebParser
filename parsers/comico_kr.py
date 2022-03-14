from parsers.basic_parser import basic_parser
# https://www.comico.kr/comic/3593/chapter/12/product

class comico_kr(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)

        import time, sys
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--disable-features=VizDisplayCompositor")
        if sys.platform.startswith('linux'):
            options.add_argument('--password-store=gnome')
        options.add_argument("--user-data-dir=" + self.config['path_to_browser'])

        ex_path = self.get_chromedriver_path()

        browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
        browser.minimize_window()

        old_title = ''

        try:
            browser.execute_script('window.stop();')
            browser.switch_to.new_window('tab')
            time.sleep(1)
            
            browser.get(self.url)

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

                images = browser.execute_script(
                    'return document.getElementsByClassName(\'viewer_comic\')[0].getElementsByTagName(\'style\');')

                images = [el.get_attribute('innerHTML') for el in images]
                
                images = [el[el.index('https://') : el.index('\');')] for el in images if '0px' not in el.split()]
                
                self.full_download(images, title)
                time.sleep(10)
                if self.chapter_count > 0:
                    try:
                        old_title = title
                        browser.execute_script('document.getElementsByClassName(\'link_next\')[0].click();')
                        self.save_folder = self.true_save_folder
                        max_wait = 10

                        while title == old_title and max_wait > 0:
                            title = browser.execute_script('return document.getElementsByClassName(\'tit_comic\')[0].textContent;')
                            max_wait -= 1
                            time.sleep(1)
                    finally: pass
                else: break
        finally:
            browser.close()
            browser.quit()
