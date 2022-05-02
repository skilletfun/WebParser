from unittest import TestCase, main
import os, shutil
from parsers.page_kakao_com import page_kakao_com
from tests.config import config, attrs


class KakaoTest(TestCase):
    def setUp(self):
        self.site = page_kakao_com(config, 'trash/log.txt')
        self.attrs = attrs
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs['url'] = 'https://page.kakao.com/viewer?productId=57540660'

    def test_multi(self):
        self.attrs['chapter_count'] = '2'
        self.assertEqual(self.site.parse(self.attrs), True)


if __name__ == '__main__':
    main()