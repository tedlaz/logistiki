from decimal import Decimal
from logistiki.utils import dec, dec2gr, gr2dec


def test_text_or_None():
    assert dec("123a") == dec(0)
    assert dec(None) == dec(0)
    assert dec("123") == dec(123)
    assert dec("-1.23") == dec(-1.23)


def test_dec2gr():
    assert dec2gr(dec(1234.56)) == "1.234,56"
    assert dec2gr(dec(1234567.89)) == "1.234.567,89"
    assert dec2gr(dec(-1234567.89)) == "-1.234.567,89"


def test_gr2dec():
    assert gr2dec("1.234,56") == dec("1234.56")
    assert gr2dec("1.234.567,89") == dec(1234567.89)
    assert gr2dec("-1,54") == dec(-1.54)


def test_rounding():
    assert dec("1.566") == dec(1.57)
    assert dec("1.545") == dec(1.55)
    assert dec("1.2445") == dec(1.24)
    assert dec("-1.2445") == dec(-1.24)


def test_different_decimals():
    assert dec("100.256") == Decimal("100.26")
    assert dec("100.256", 2) == Decimal("100.26")
    assert dec("100.256", 1) == Decimal("100.3")
    assert dec("100.256", 0) == Decimal("100.3")
    assert dec("100.256", -3) == Decimal("100.3")
