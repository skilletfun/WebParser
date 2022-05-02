from unittest import TestCase, main
import os, shutil
from parsers.mangareader_to import mangareader_to
from tests.config import config, attrs


class MangareaderTest(TestCase):
    def setUp(self):
        self.site = mangareader_to(config, 'trash/log.txt')
        self.attrs = attrs
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs['url'] = 'https://mangareader.to/read/bleach-color-edition-55958/en/chapter-1'

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