from unittest import TestCase
# from decimal import Decimal
from logistiki.dec import dec, dec2gr, gr2dec


class TestsDec(TestCase):
    def test_text_or_None(self):
        self.assertEqual(dec('123a'), dec(0))
        self.assertEqual(dec(None), dec(0))
        self.assertEqual(dec('123'), dec(123))
        self.assertEqual(dec('-1.23'), dec(-1.23))

    def test_dec2gr(self):
        self.assertEqual(dec2gr(dec(1234.56)), '1.234,56')
        self.assertEqual(dec2gr(dec(1234567.89)), '1.234.567,89')
        self.assertEqual(dec2gr(dec(-1234567.89)), '-1.234.567,89')

    def test_gr2dec(self):
        self.assertEqual(gr2dec('1.234,56'), dec('1234.56'))
        self.assertEqual(gr2dec('1.234.567,89'), dec(1234567.89))
        self.assertEqual(gr2dec('-1,54'), dec(-1.54))

    def test_rounding(self):
        self.assertEqual(dec('1.566'), dec(1.57))
        self.assertEqual(dec('1.545'), dec(1.55))
        self.assertEqual(dec('1.2445'), dec(1.24))
        self.assertEqual(dec('-1.2445'), dec(-1.24))
