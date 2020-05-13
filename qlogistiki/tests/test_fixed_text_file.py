import os
import unittest
from qlogistiki import fixed_text_file as ftf

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestFixedTestFile(unittest.TestCase):
    def test_001(self):
        bfile = os.path.join(dir_path, 'CSL01')
        apd = ftf.apd_builder()
        apd.parse(bfile)
        v1 = ftf.ColTextCapital()
        t1 = v1.render('αργυρίου', 10)
        self.assertEqual(t1, 'ΑΡΓΥΡΙΟΥ  ')

        # print(apd.lines)
        self.assertTrue(apd.check())
        rval = apd.render()
        self.assertTrue(rval.startswith('10101CSL01   0101218ΠΑΡΟΥ'))
        self.assertEqual(rval[-3:], 'EOF')
        self.assertEqual(
            apd.linetype_names,
            [
                'Header',
                'Stoixeia Ergazomenoy',
                'Stoixeia misthodosias',
                'Terminator line'
            ]
        )
        # do1.malakia()
        # apd.correct_header()
        # apd.render2file('CSL01-corrected')
        # print(apd)
        # print(apd.linetypes_report())
