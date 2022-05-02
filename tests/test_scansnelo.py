from unittest import TestCase, main
import os, shutil
from parsers.scansnelo_com import scansnelo_com
from tests.config import config, attrs


class ScansneloTest(TestCase):
    def setUp(self):
        self.site = scansnelo_com(config, 'trash/log.txt')
        self.attrs = attrs
        self.attrs['url'] = 'https://mangafunny.net/manga/my-senior-brother-is-too-steady/chapter-1/'

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