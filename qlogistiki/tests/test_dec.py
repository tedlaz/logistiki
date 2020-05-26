from qlogistiki.dec import Dec


def test_dec_of_string():
    assert Dec('aaasf') == 0


def test_dec_of_None():
    assert Dec(None) == 0


def test_dec_of_0():
    assert Dec(0) == 0


def test_dec_of_float():
    assert Dec(123.45) == 123.45


def test_dec_of_negative_float():
    assert Dec(-123.45) == -123.45


def test_dec_of_str_num():
    assert Dec('123.45') == 123.45


def test_dec_of_negative_str_num():
    assert Dec('-123.45') == -123.45


def test_dec_round_01():
    assert Dec('123.4554') == 123.46


def test_dec_round_01():
    assert Dec('123.4554') == 123.46


def test_dec_round_01():
    assert Dec('-123.4554') == -123.46


def test_sum_decs():
    assert Dec(1.35) + Dec('1.2') == 2.55


def test_sum_decs_negative_01():
    assert Dec(1.35) + Dec('-1.2') == 0.15


def test_sum_decs_negative_02():
    assert Dec(-1.35) + Dec('-1.2') == -2.55


def test_sum_dec_int():
    assert Dec(134.54) + 100 == Dec('234.54')


def test_sum_int_dec():
    assert 1000.41 + Dec(134.54) == Dec('1134.95')


def test_sum_dec_float():
    assert Dec(134.54) + 100.02 == Dec('234.56')


def test_sum_foat_dec():
    assert 144 + Dec(134.54) == Dec('278.54')


def test_dec_sub():
    assert Dec(1.35) - Dec(1) == .35
    assert Dec(1.35) - 1 == .35
    assert 1.35 - Dec(1) == .35


def test_mul():
    assert Dec(100.25) * 4 == 401
    assert 100.25 * Dec(4) == 401
    assert Dec(40) * 1.5 == 60
    assert 40 * Dec(1.5) == Dec(60)


def test_truediv():
    assert Dec(40) / 2 == 20
    assert 40 / Dec(2) == 20
    assert 40.0 / Dec(2) == 20


def test_neg():
    assert -Dec(40) == -40
    assert -Dec(-40) == 40


def test_abs():
    assert abs(Dec(40)) == 40
    assert abs(Dec(-40)) == 40
    assert abs(Dec(-0)) == 0


def test_complex():
    assert (Dec(1.5) + 1) * 2 == 5


def test_eq():
    assert Dec('test') == 0
    assert Dec('123.245') == 123.25
    assert Dec('123.245') == Dec(123.25)
    assert Dec(-123.245) == -123.25


def test_gt():
    assert Dec(1) > 0
    assert 1 > Dec(0)


def test_ge():
    assert Dec(1) >= 0
    assert 1 >= Dec(0)
    assert Dec(0) >= 0
    assert 1 >= Dec(1)


def test_repr():
    assert repr(Dec(123)) == 'Dec(123.00)'
    assert repr(Dec(0)) == 'Dec(0.00)'
    assert repr(Dec('just-text')) == 'Dec(0.00)'


def test_from_gr():
    assert Dec.from_gr('1.234,565') == 1234.57
    assert Dec.from_gr(',565') == .57
    assert Dec.from_gr(',565g') == 0


def test_gr0():
    assert Dec().gr0 == '0,00'
    assert Dec(123456.78).gr0 == '123.456,78'
    assert Dec(123456.).gr0 == '123.456,00'
    assert Dec(123456.7).gr0 == '123.456,70'
    assert Dec(-123456.7).gr0 == '-123.456,70'


def test_gr():
    assert Dec().gr == ''
    assert Dec(123456.78).gr == '123.456,78'
    assert Dec(123456.).gr == '123.456,00'
    assert Dec(123456.7).gr == '123.456,70'
    assert Dec(-123456.7).gr == '-123.456,70'


def test_grs():
    assert Dec().grs == '0   '
    assert Dec(123).grs == '123   '
    assert Dec(-123).grs == '-123   '
    assert Dec(123.50).grs == '123,5 '
    assert Dec(123.51).grs == '123,51'
    assert Dec(123456.789).grs == '123.456,79'
    assert Dec(-1234567.89).grs == '-1.234.567,89'


def test_general():
    vl1 = Dec(10.23)
    vl2 = Dec(16.77)
    assert vl1 + vl2 == 27
