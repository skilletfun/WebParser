from unittest import TestCase, main
import os, shutil
from parsers.bomtoon_com import bomtoon_com
from tests.config import config, attrs


class BomtoonTest(TestCase):
    def setUp(self):
        self.site = bomtoon_com(config, 'trash/log.txt')
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs = attrs
        self.attrs['url'] = 'https://www.bomtoon.com/comic/ep_view/tlawkddprp/01'

    # def tearDown(self):
    #     for file in os.listdir('trash'):
    #         file = os.path.join('trash', file)
    #         if os.path.isfile(file): os.remove(file)
    #         else: shutil.rmtree(file)

    def test_one(self):
        self.assertEqual(self.site.parse(self.attrs), True)


if __name__ == '__main__':
    main()