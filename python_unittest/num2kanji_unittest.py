import unittest
import requests

url = "https://kanjinumbers.azurewebsites.net/api/v1/num2kanji/"
# url = "http://localhost:7071/api/v1/num2kanji/"


def n2k(num):
    res = requests.get(url + str(num))
    status_code = res.status_code
    return res.json() if status_code == 200 else status_code


class N2KNormalTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(n2k(100), "壱百")

    def test2(self):
        self.assertEqual(n2k(0), "零")

    def test3(self):
        self.assertEqual(n2k(3), "参")

    def test4(self):
        self.assertEqual(n2k(90238481), "九千弐拾参万八千四百八拾壱")

    def test5(self):
        self.assertEqual(n2k(1000000000000000), "壱千兆")

    def test6(self):
        self.assertEqual(n2k(4000000100006), "四兆壱拾万六")

    def test7(self):
        self.assertEqual(n2k(10100100010000), "壱拾兆壱千壱億壱万")

    def test8(self):
        self.assertEqual(n2k(9999999999999999), "九千九百九拾九兆九千九百九拾九億九千九百九拾九万九千九百九拾九")

    def test9(self):
        self.assertEqual(n2k(1), "壱")

    def test10(self):
        self.assertEqual(n2k(10), "壱拾")

    def test11(self):
        self.assertEqual(n2k(101), "壱百壱")

    def test12(self):
        self.assertEqual(n2k(1010), "壱千壱拾")

    def test13(self):
        self.assertEqual(n2k(10947), "壱万九百四拾七")


class N2KErrorTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(n2k("fre"), 204)

    def test2(self):
        self.assertEqual(n2k("34f33"), 204)

    def test3(self):
        self.assertEqual(n2k(74893787979438921798074), 204)

    def test4(self):
        self.assertEqual(n2k(-34), 204)

    def test5(self):
        self.assertEqual(n2k(9999999999999999 + 1), 204)
