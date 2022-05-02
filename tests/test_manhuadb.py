from unittest import TestCase, main
import os, shutil
from parsers.manhuadb_com import manhuadb_com
from tests.config import config, attrs


class ManhuadbTest(TestCase):
    def setUp(self):
        self.site = manhuadb_com(config, 'trash/log.txt')
        self.attrs = attrs
        self.attrs['url'] = 'https://www.manhuadb.com/manhua/1025/1079_10796.html'

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