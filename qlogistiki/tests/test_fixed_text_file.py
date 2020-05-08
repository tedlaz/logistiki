import os
import unittest
from qlogistiki import fixed_text_file as ftf

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestFixedTestFile(unittest.TestCase):
    def test_001(self):
        bfile = os.path.join(dir_path, 'CSL01')
        apd = ftf.apd_builder()
        apd.parse(bfile)
        # print(apd.lines)
        # print(apd.check())
        # print(apd.render())
        # do1.malakia()
        # do1.correct_header()
        # print(apd)
        # apd.print_lines()
