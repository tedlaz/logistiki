import os
import unittest
from qlogistiki import data_operations_text as dot

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestDataOperationsText(unittest.TestCase):
    def test_001(self):
        bfile = os.path.join(dir_path, 'booktst.txt')
        book = dot.load_from_text(bfile)
        btxt = dot.save_dummy(book)
        self.assertTrue(btxt.startswith('$ 111222333 Μαλακόπουλος ΕΠΕ'))
        self.assertTrue(btxt[-16:-2], 'Μετρητά.Ταμείο')
