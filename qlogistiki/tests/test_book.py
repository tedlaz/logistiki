import unittest
import os
from qlogistiki.book import Book

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestBoon(unittest.TestCase):
    def test_001(self):
        fil = "/run/user/1000/gvfs/smb-share:server=trancend-red,share=sda1/documents/ted-data/tedata"
        b01 = Book('111222333', 'TestCo')
        bfile = os.path.join(dir_path, 'spiros.txt')
        # bfile = os.path.join(dir_path, fil)
        # b01.parse(bfile)
        # b01.isozygio_afm()
        # 0: Χωρίς ΦΠΑ, 1: ΦΠΑ οκ, 2: ΦΠΑ λάθος
        # b01.fpa_status()
        # print(b01.transactions[0])
        # b01.write2file('makakia.txt')