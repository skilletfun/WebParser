from unittest import TestCase, main
import os, shutil
from parsers.ac_qq_com import ac_qq_com
from tests.config import config, attrs


class AcqqcomTest(TestCase):
    def setUp(self):
        self.site = ac_qq_com(config)
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs = attrs
        self.attrs['url'] = 'https://ac.qq.com/ComicView/index/id/631605/cid/1'

    def tearDown(self):
        for file in os.listdir('trash'):
            file = os.path.join('trash', file)
            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)

    def test_one(self):
        self.assertEqual(self.site.parse(self.attrs), True)

    def test_multi(self):
        self.attrs['chapter_count'] = '2'
        self.assertEqual(self.site.parse(self.attrs), True)


if __name__ == '__main__':
    main()