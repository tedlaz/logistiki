import unittest
import os
from qlogistiki.book import Book

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestBoon(unittest.TestCase):
    def test_001(self):
        b01 = Book('111222333', 'TestCo', [], None, None)
        bfile = os.path.join(dir_path, 'booktst.txt')
        # bfile = os.path.join(dir_path, fil)
        # b01.parse(bfile)
        # b01.isozygio_afm()
        # 0: Χωρίς ΦΠΑ, 1: ΦΠΑ οκ, 2: ΦΠΑ λάθος
        # b01.fpa_status()
        # print(b01.transactions[0])
        # b01.write2file('makakia.txt')
