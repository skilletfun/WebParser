from parsers.basic_parser import basic_parser


class comic_naver_com(basic_parser):
    def parse(self, attrs):

        self.update_vars(attrs)
        
        if 'weekday' in self.url:
            self.url = self.url[:self.url.find('weekday') - 1]
            
        old_url = ''
            
        while True:
            self.chapter_count -= self.step
            
            headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
            response = requests.get(self.url, headers=headers)
                    
            if 'list?titleId' in response.url or old_url == self.url:
                break
                
            src = response.text
            
            title, images = self.find_images(src, 'div', 'class', 'wt_viewer')
            
            title += str(int(self.url[self.url.rfind('=') + 1:]))

            images = [img.get('src') for img in images]
            
            self.full_download(images, title)

            if self.chapter_count > 0:
                old_url = self.url
                self.url = self.url[:self.url.rfind('=') + 1] + str(int(self.url[self.url.rfind('=') + 1:]) + 1)
                self.save_folder = self.true_save_folder
            else:
                break
