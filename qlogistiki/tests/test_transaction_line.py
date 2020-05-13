import unittest
from qlogistiki.transaction_line import TransactionLine


class TestTransactionLine(unittest.TestCase):
    def test_tr001(self):
        tl1 = TransactionLine('Aa.Bb.Cc', -100)
        tl2 = TransactionLine('Aa.Bb.Cc', -100)
        self.assertTrue(tl1 == tl2)
        self.assertEqual(tl1.debit, 0)
        self.assertEqual(tl1.credit, 100)
        self.assertEqual(tl1.delta, -100)
        self.assertEqual(tl1 * -2, TransactionLine('Aa.Bb.Cc', 200))
        self.assertEqual(1.5 * tl2, tl2 * 1.5)
