from unittest import TestCase, main
import os, shutil
from parsers.comic_naver_com import comic_naver_com
from tests.config import config, attrs


class NaverTest(TestCase):
    def setUp(self):
        self.site = comic_naver_com(config)
        self.attrs = attrs
        self.attrs['url'] = 'https://comic.naver.com/webtoon/detail?titleId=746834&no=90&weekday=sat'

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