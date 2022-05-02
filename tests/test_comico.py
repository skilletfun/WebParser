from unittest import TestCase, main
import os, shutil
from parsers.comico_kr import comico_kr
from tests.config import config, attrs


class ComicoTest(TestCase):
    def setUp(self):
        self.site = comico_kr(config, 'trash/log.txt')
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs = attrs
        self.attrs['url'] = 'https://www.comico.kr/comic/323/chapter/1/product'

    def tearDown(self):
        for file in os.listdir('trash'):
            file = os.path.join('trash', file)
            if os.path.isfile(file): os.remove(file)
            else: shutil.rmtree(file)

    def test_one(self):
        self.assertEqual(self.site.parse(self.attrs), True)


if __name__ == '__main__':
    main()