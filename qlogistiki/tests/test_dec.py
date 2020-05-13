import unittest
from qlogistiki.dec import Dec


class TestDec(unittest.TestCase):
    def test_creating(self):
        dc1 = Dec(123.45)
        dc2 = Dec('123.45')
        dc2 = Dec('aaaasf')

    def test_add(self):
        self.assertEqual(Dec(1.35) + Dec(1), 2.35)
        self.assertEqual(Dec(1.35) + 1, 2.35)
        self.assertEqual(1 + Dec(1.35), 2.35)

    def test_sub(self):
        self.assertEqual(Dec(1.35) - Dec(1), .35)
        self.assertEqual(Dec(1.35) - 1, .35)
        self.assertEqual(1.35 - Dec(1), .35)

    def test_mul(self):
        self.assertEqual(Dec(100.25) * 4, 401)
        self.assertEqual(100.25 * Dec(4), 401)
        self.assertEqual(Dec(40) * 1.5, 60)
        self.assertEqual(40 * Dec(1.5), Dec(60))

    def test_truediv(self):
        self.assertEqual(Dec(40) / 2, 20)
        self.assertEqual(40 / Dec(2), 20)
        self.assertEqual(40.0 / Dec(2), 20)

    def test_neg(self):
        self.assertEqual(-Dec(40), -40)
        self.assertEqual(-Dec(-40), 40)

    def test_abs(self):
        self.assertEqual(abs(Dec(40)), 40)
        self.assertEqual(abs(Dec(-40)), 40)
        self.assertEqual(abs(Dec(-0)), 0)

    def test_eq(self):
        self.assertEqual(Dec('test'), 0)
        self.assertEqual(Dec('123.245'), 123.25)
        self.assertEqual(Dec('123.245'), Dec(123.25))
        self.assertEqual(Dec(-123.245), -123.25)

    def test_gt(self):
        self.assertTrue(Dec(1) > 0)
        self.assertTrue(1 > Dec(0))

    def test_ge(self):
        self.assertTrue(Dec(1) >= 0)
        self.assertTrue(1 >= Dec(0))
        self.assertTrue(Dec(0) >= 0)
        self.assertTrue(1 >= Dec(1))

    def test_repr(self):
        self.assertEqual(repr(Dec(123)), 'Dec(123.00)')
        self.assertEqual(repr(Dec(0)), 'Dec(0.00)')
        self.assertEqual(repr(Dec('just-text')), 'Dec(0.00)')

    def test_from_gr(self):
        self.assertEqual(Dec.from_gr('1.234,565'), 1234.57)
        self.assertEqual(Dec.from_gr(',565'), .57)
        self.assertEqual(Dec.from_gr(',565g'), 0)

    def test_gr0(self):
        self.assertEqual(Dec().gr0, '0,00')
        self.assertEqual(Dec(123456.78).gr0, '123.456,78')
        self.assertEqual(Dec(123456.).gr0, '123.456,00')
        self.assertEqual(Dec(123456.7).gr0, '123.456,70')
        self.assertEqual(Dec(-123456.7).gr0, '-123.456,70')

    def test_gr(self):
        self.assertEqual(Dec().gr, '')
        self.assertEqual(Dec(123456.78).gr, '123.456,78')
        self.assertEqual(Dec(123456.).gr, '123.456,00')
        self.assertEqual(Dec(123456.7).gr, '123.456,70')
        self.assertEqual(Dec(-123456.7).gr, '-123.456,70')

    def test_grs(self):
        self.assertEqual(Dec().grs, '0   ')
        self.assertEqual(Dec(123).grs, '123   ')
        self.assertEqual(Dec(-123).grs, '-123   ')
        self.assertEqual(Dec(123.50).grs, '123,5 ')
        self.assertEqual(Dec(123.51).grs, '123,51')
        self.assertEqual(Dec(123456.789).grs, '123.456,79')
        self.assertEqual(Dec(-1234567.89).grs, '-1.234.567,89')

    def test_general(self):
        vl1 = Dec(10.23)
        vl2 = Dec(16.77)
        self.assertEqual(vl1 + vl2, 27)
