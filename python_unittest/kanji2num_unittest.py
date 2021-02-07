import unittest
import requests

url = "https://kanjinumbers.azurewebsites.net/api/v1/kanji2num/"
# url = "http://localhost:7071/api/v1/kanji2num/"


def k2n(kanji):
    res = requests.get(url + str(kanji))
    status_code = res.status_code
    return res.json() if status_code == 200 else status_code


class K2NNormalTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(k2n("四百参拾弐兆四千参百弐拾七億四千九百参拾七万八千四百弐拾参"), 432432749378423)

    def test2(self):
        self.assertEqual(k2n("九兆弐億参千八百四拾八万壱千壱百壱拾壱"), 9000238481111)

    def test3(self):
        self.assertEqual(k2n("壱千兆"), 1000000000000000)

    def test4(self):
        self.assertEqual(k2n("零"), 0)

    def test5(self):
        self.assertEqual(k2n("壱千四億五千参万"), 100450030000)

    def test6(self):
        self.assertEqual(k2n("壱拾壱"), 11)

    def test7(self):
        self.assertEqual(k2n("四百参拾"), 430)

    def test8(self):
        self.assertEqual(k2n("四兆壱拾万参"), 4000000100003)


class K2NErrorTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(k2n("拾"), 204)

    def test2(self):
        self.assertEqual(k2n("兆"), 204)

    def test3(self):
        self.assertEqual(k2n("拾壱"), 204)

    def test4(self):
        self.assertEqual(k2n("零零"), 204)

    def test5(self):
        self.assertEqual(k2n("壱千四億五億千参万"), 204)  # 億の後ろに億

    def test6(self):
        self.assertEqual(k2n("壱千四億五億千参万七兆四"), 204)  # 億の後ろに億と兆

    def test7(self):
        self.assertEqual(k2n("四千七万億五千参"), 204)  # 万の後ろに億

    def test8(self):
        self.assertEqual(k2n("壱千四億五四億千参万"), 204)  # 五四が連続

    def test9(self):
        self.assertEqual(k2n("不正な文字"), 204)

    def test10(self):
        self.assertEqual(k2n("四千一"), 204)  # 一ではなく壱

    def test11(self):
        self.assertEqual(k2n("四千a五"), 204)

    def test12(self):
        self.assertEqual(k2n(100), 204)
