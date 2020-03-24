from unittest import TestCase
from logistiki.transaction_line import TransactionLine, dec


class TestsTline(TestCase):
    def test_001(self):
        lin = TransactionLine.new_by_code('38.00.00', 1, 100.25)
        self.assertEqual(lin.credit, 0)
        self.assertEqual(lin.debit, 100.25)
        self.assertEqual(lin.flat_value, 100.25)

    def test_002(self):
        lin = TransactionLine.new_by_code('38.00.00', 2, 53.45)
        self.assertEqual(lin.credit, dec(53.45))
        self.assertEqual(lin.debit, 0)
        self.assertEqual(lin.flat_value, dec(-53.45))

    def test_dec(self):
        self.assertEqual(str(dec(0)), '0.00')
        self.assertEqual(str(dec(7.325)), '7.33')
        self.assertEqual(str(dec(1.325)), '1.32')
        self.assertEqual(str(dec(1.344)), '1.34')
        self.assertEqual(str(dec(1.995)), '2.00')

    def test_equality(self):
        li1 = TransactionLine.new_by_code('38.00.00', 2, 53.45)
        li2 = TransactionLine.new_by_code('38.00.00', 2, 53.45)
        li3 = TransactionLine.new_by_code('38.00.01', 2, 53.45)
        li4 = TransactionLine.new_by_code('38.00.00', 1, 53.45)
        li5 = TransactionLine.new_by_code('38.00.00', 2, 53.46)
        self.assertEqual(li1, li2)
        self.assertNotEqual(li1, li3)
        self.assertNotEqual(li1, li4)
        self.assertNotEqual(li1, li5)
        self.assertTrue(li1 < li3)
