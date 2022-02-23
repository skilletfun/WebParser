from parsers.basic_parser import basic_parser

class rawdevart_com(basic_parser):
    def parse(self, attrs):
        self.update_vars(attrs)
        src = self.get_response(self.url)

        title, images = self.find_images(src, 'div', 'id', 'img-container')

        images = [img.get('data-src') for img in images]

        self.full_download(images, title)