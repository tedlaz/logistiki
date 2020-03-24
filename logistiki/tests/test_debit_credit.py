from unittest import TestCase
from logistiki.debit_credit import DebitCredit


class TestsDebitCredit(TestCase):
    def test_001(self):
        v1 = DebitCredit(2, 30.0)
        v2 = DebitCredit(1, 20)
        v3 = DebitCredit(1, -30)
        v4 = DebitCredit.new_by_dc(0, -100)
        self.assertEqual(v1, v3)
        self.assertEqual(v3, v1)
        self.assertEqual(v4, v4.negatived())
        self.assertEqual(v3, v3.positived())
        self.assertEqual(v1 + v2, DebitCredit(2, 10))
        self.assertEqual(v1 - v2, DebitCredit(2, 50))
        self.assertEqual(v1 - v1, DebitCredit(1, 0))
        self.assertEqual(v1 - v1, DebitCredit(2, 0))
        self.assertEqual(DebitCredit(1, 0), DebitCredit(2, 0))
        self.assertEqual(v1 * 1.5, DebitCredit(2, 45))
        self.assertEqual(v2 / 2, DebitCredit(1, 10))
        self.assertFalse(v1 > v2)
        self.assertTrue(v1 < v2)

    def test_002(self):
        v1 = DebitCredit(1, 12560.278)
        self.assertEqual(v1.ypoloipo, '12.560,28')
        self.assertEqual((-v1).ypoloipo, '-12.560,28')
        v2 = DebitCredit(2, 20)
        self.assertEqual(v2.pistosi_positive, '20,00')
        self.assertEqual(v2.xreosi_negative, '-20,00')
        self.assertEqual(v2.real_dc, 2)
        v3 = DebitCredit(2, -40)
        self.assertEqual(v3.real_dc, 1)
        self.assertEqual(v3.xreosi_positive, '40,00')
        self.assertEqual(v3.pistosi_negative, '-40,00')
