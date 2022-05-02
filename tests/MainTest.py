import os
from unittest import TestSuite, TextTestRunner, makeSuite
from tests.test_webtoons import WebtoonsTest
from tests.test_ac_qq_com import AcqqcomTest
from tests.test_bomtoon import BomtoonTest
from tests.test_comic_naver import NaverTest
from tests.test_comico import ComicoTest
from tests.test_fanfox import FanfoxTest
from tests.test_mangakakalot import MangakakalotTest
from tests.test_kuaikanmanhua import KuaikanmanhuaTest
from tests.test_mangareader import MangareaderTest
from tests.test_ridibooks import RidibooksTest
from tests.test_kakao import KakaoTest


if __name__ == '__main__':
    tester = TestSuite()

    # tester.addTest(makeSuite(WebtoonsTest))           # Completed
    # tester.addTest(makeSuite(AcqqcomTest))            # Completed
    # tester.addTest(makeSuite(BomtoonTest))            # Completed
    # tester.addTest(makeSuite(NaverTest))              # Completed
    # tester.addTest(makeSuite(ComicoTest))             # Completed
    # tester.addTest(makeSuite(FanfoxTest))             # Completed
    # tester.addTest(makeSuite(MangakakalotTest))       # Completed
    # tester.addTest(makeSuite(KuaikanmanhuaTest))      # Completed
    # tester.addTest(makeSuite(MangareaderTest))        # Completed
    # tester.addTest(makeSuite(RidibooksTest))          # Completed
    # tester.addTest(makeSuite(KakaoTest))              # Completed

    runner = TextTestRunner(verbosity=2)
    runner.run(tester)