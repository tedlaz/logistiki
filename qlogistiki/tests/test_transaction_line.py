from qlogistiki.transaction_line import TransactionLine


def test_tr001():
    tl1 = TransactionLine("Aa.Bb.Cc", -100)
    tl2 = TransactionLine("Aa.Bb.Cc", -100)
    assert tl1 == tl2
    assert tl1.debit == 0
    assert tl1.credit == 100
    assert tl1.delta == -100
    assert tl1 * -2 == TransactionLine("Aa.Bb.Cc", 200)
    assert 1.5 * tl2 == tl2 * 1.5
