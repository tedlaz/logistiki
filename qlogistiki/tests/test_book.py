import unittest
import os
from qlogistiki.book import Book

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestBoon(unittest.TestCase):
    def test_001(self):
        b01 = Book('111222333', 'TestCo')
        bfile = os.path.join(dir_path, 'spiros.txt')
        b01.parse(bfile)
        b01.isozygio_afm()
        b01.fpa_status()
