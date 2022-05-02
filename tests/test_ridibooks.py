from unittest import TestCase, main
import os, shutil
from parsers.ridibooks_com import ridibooks_com
from tests.config import config, attrs


class RidibooksTest(TestCase):
    def setUp(self):
        self.site = ridibooks_com(config, 'trash/log.txt')
        self.attrs = attrs
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs['url'] = 'https://view.ridibooks.com/books/4873000001'

    def tearDown(self):
        for file in os.listdir('trash'):
            file = os.path.join('trash', file)
            if os.path.isfile(file): os.remove(file)
            else: shutil.rmtree(file)

    def test_multi(self):
        self.attrs['chapter_count'] = '2'
        self.assertEqual(self.site.parse(self.attrs), True)


if __name__ == '__main__':
    main()