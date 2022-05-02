from unittest import TestCase, main
import os, shutil
from parsers.webtoons_com import webtoons_com
from tests.config import config, attrs


class WebtoonsTest(TestCase):
    def setUp(self):
        self.site = webtoons_com(config, 'trash/log.txt')
        self.attrs = attrs
        self.attrs['url'] = 'https://www.webtoons.com/en/slice-of-life/hyperfocus/ep-11-walking-home/viewer?title_no=3340&episode_no=11'

    def tearDown(self):
        for file in os.listdir('trash'):
            file = os.path.join('trash', file)
            if os.path.isfile(file): os.remove(file)
            else: shutil.rmtree(file)

    # def test_one(self):
    #     self.assertEqual(self.site.parse(self.attrs), True)

    def test_multi(self):
        self.attrs['chapter_count'] = '2'
        self.assertEqual(self.site.parse(self.attrs), True)


if __name__ == '__main__':
    main()