from parsers.basic_parser import basic_parser
import sys

class kuaikanmanhua_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("window-size=900,600")

        ex_path = self.get_chromedriver_path()

        browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)

        try:
            while True:
                self.chapter_count -= self.step
                browser.get(self.url)
                src = browser.page_source

                title, images = self.find_images(src, 'div', 'class', 'imgList')

                images = [img.get('data-src') for img in images if not img.get('data-src') is None]

                self.full_download(images, title)

                if self.chapter_count > 0:
                    res = self.find_element(src, 'div', 'class', 'AdjacentChapters').find_all('a')[-1]
                    if 'javascript' not in res:
                        self.url = 'https://www.kuaikanmanhua.com' + res.get('href')
                        self.save_folder = self.true_save_folder
                    else:
                        break
                else:
                    break
        finally:
            browser.close()
            browser.quit()
