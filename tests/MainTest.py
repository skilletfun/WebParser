import os
from unittest import TestSuite, TextTestRunner, makeSuite
from tests.test_webtoons import WebtoonsTest
from tests.test_ac_qq_com import AcqqcomTest
from tests.test_bomtoon import BomtoonTest
from tests.test_comic_naver import NaverTest
from tests.test_comico import ComicoTest


if __name__ == '__main__':
    tester = TestSuite()

    # tester.addTest(makeSuite(WebtoonsTest))
    # tester.addTest(makeSuite(AcqqcomTest))
    # tester.addTest(makeSuite(BomtoonTest))
    # tester.addTest(makeSuite(NaverTest))
    tester.addTest(makeSuite(ComicoTest))
    # tester.addTest(makeSuite(FanfoxTest))

    runner = TextTestRunner(verbosity=2)
    runner.run(tester)