from unittest import TestCase
from qlogistiki import utils as utl
from qlogistiki.utils import grup


class TestUtils(TestCase):
    def test_gr_num(self):
        self.assertEqual(utl.gr_num(1010.34), '1.010,34')
        self.assertEqual(utl.gr_num(0), '0   ')
        self.assertEqual(utl.gr_num(123123.50), '123.123,5 ')
        self.assertEqual(utl.gr_num(-123123.50), '-123.123,5 ')
        self.assertEqual(utl.gr_num(.01), '0,01')
        self.assertEqual(utl.gr_num(-.01), '-0,01')
        self.assertEqual(utl.gr_num(.10), '0,1 ')
        self.assertEqual(utl.gr_num(-82.00), '-82   ')
        self.assertEqual(utl.gr_num('rt'), '0   ')
        self.assertEqual(utl.gr_num(None), '0   ')

    def test_account_tree(self):
        self.assertEqual(utl.account_tree('a.b.c'), ('a', 'a.b', 'a.b.c'))
        self.assertEqual(utl.account_tree('a'), ('a',))
        self.assertEqual(utl.account_tree(''), ('',))
        self.assertEqual(utl.account_tree(1), ('',))
        self.assertEqual(utl.account_tree('a.b', True), ('a.b', 'a'))

    def test_grup(self):
        self.assertEqual(grup('ΐέάό'), 'ΙΕΑΟ')
        self.assertEqual(grup('Ίώνάς'), 'ΙΩΝΑΣ')
        self.assertEqual(grup('ϊίΫώrock123'), 'ΙΙΥΩROCK123')

    def test_is_afm(self):
        self.assertTrue(utl.is_afm('094025817'))
        self.assertFalse(utl.is_afm('094025818'))
        self.assertFalse(utl.is_afm('0'))
        self.assertFalse(utl.is_afm('0940258179'))
