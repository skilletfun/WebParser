from unittest import TestCase, main
import os, shutil
from parsers.kuaikanmanhua_com import kuaikanmanhua_com
from tests.config import config, attrs


class KuaikanmanhuaTest(TestCase):
    def setUp(self):
        self.site = kuaikanmanhua_com(config, 'trash/log.txt')
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs = attrs
        self.attrs['url'] = 'https://www.kuaikanmanhua.com/web/comic/252117/'

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