from parsers.basic_parser import basic_parser

class scansnelo_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        
        while True:
            self.chapter_count -= self.step
            src = self.get_response(self.url)

            title, images = self.find_images(src, 'div', 'class', 'reading-content')

            images = [img.get('src').strip() for img in images]
            
            self.full_download(images, title)

            if self.chapter_count > 0:
                res = self.find_element(src, 'a', 'class', 'next_page')
                if not res is None:
                    self.url = res.get('href')
                    self.save_folder = self.true_save_folder
                else: break
            else: break
