from unittest import TestCase, main
import os, shutil
from parsers.fanfox_net import fanfox_net
from tests.config import config, attrs


class FanfoxTest(TestCase):
    def setUp(self):
        self.site = fanfox_net(config, 'trash/log.txt')
        self.site.set_chromedriver_path('../chromedriver')
        self.attrs = attrs
        self.attrs['url'] = 'https://fanfox.net/manga/the_lazy_prince_becomes_a_genius/c001/1.html#ipg1'

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