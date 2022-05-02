from unittest import TestCase, main
import os, shutil
from parsers.rawdevart_com import rawdevart_com
from tests.config import config, attrs


class RawdevartTest(TestCase):
    def setUp(self):
        self.site = rawdevart_com(config, 'trash/log.txt')
        self.attrs = attrs
        self.attrs['url'] = 'https://rawdevart.com/comic/yuujin-character-wa-taihen-desu-ka/chapter-27/'

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