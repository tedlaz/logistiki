from unittest import TestCase
from logistiki.transaction import Transaction, TranTotals, difference


class TestsTline(TestCase):
    def test_001(self):
        trn = Transaction('2019-01-01', 'ΤΔΑ35', 'Δοκιμή')
        trn.add_line('70.00.024', 2, 100)
        trn.add_line('54.00.724', 2, 24)
        trn.add_final('30.00.000')
        self.assertEqual(trn.totals, TranTotals(124, 124, 0, 3))

    def test_002(self):
        trn = Transaction('2019-01-02', 'ΤΔΑ122', 'Δοκιμή')
        trn.add_line('70.00.024', 1, -100)
        trn.add_line('54.00.724', 1, -24)
        trn.add_final('30.00.000')
        # print(trn)
        # print(trn, trn.new_normal, trn.new_negative, trn.to_ee)
        self.assertTrue(trn.new_normal == trn.new_negative)

    def test_003(self):
        # tr1
        tr1 = Transaction('2019-01-02', 'ΤΔΑ122', 'Δοκιμή')
        tr1.add_line('70.00.024', 1, -100)
        tr1.add_line('54.00.724', 1, -24)
        tr1.add_final('30.00.000')
        # tr2
        tr2 = Transaction('2019-01-02', 'ΤΔΑ122', 'Δοκιμή')
        tr2.add_line('70.00.024', 2, 100)
        tr2.add_line('54.00.724', 2, 24)
        tr2.add_final('30.00.000')
        # tr3
        tr3 = Transaction('2019-01-02', 'ΤΔΑ122', 'Δοκιμή')
        tr3.add_line('70.00.024', 2, 100)
        tr3.add_line('54.00.724', 1, -24)
        tr3.add_line('30.00.000', 2, -124)
        self.assertEqual(tr1, tr2)
        self.assertEqual(tr1, tr3)
        self.assertTrue(tr1.new_negative == tr2)
        # print(tr1, tr2, tr1 + tr2, -tr1 + tr1)
        # print(tr1 * 1.25)

    def test_004(self):
        tr1 = Transaction('2019-03-15', 'ΤΔΑ335', 'Πωλήσεις εμπορευμάτων')
        tr1.add_calculated('70.00.024', '54.00.024', 2, 0.03, .24)
        tr1.add_calculated('70.00.013', '54.00.013', 2, 0.04, .13)
        tr1.add_final('30.00.000')
        self.assertEqual(tr1.totals.counter, 5)

    def test_transaction_from_dic(self):
        dic = {
            'date': '2020-03-03', 'par': 'ΤΔΑ3', 'per': 'Δοκιμή τεστ',
            'afm': '123123123',
            'lines': [
                {'account': '20.00.013', 'typ': 1, 'value': 100},
                {'account': '54.00.213', 'typ': 1, 'value': 13},
                {'account': '50.00.001', 'typ': 2, 'value': 113},
            ]
        }
        tr1 = Transaction.tran_from_dic(dic)
        tr2 = Transaction('2020-03-03', 'ΤΔΑ3', 'Δοκιμή τεστ', '123123123')
        tr2.add_line('50.00.001', 2, 113)
        tr2.add_line('54.00.213', 1, 13)
        tr2.add_line('20.00.013', 1, 100)
        self.assertEqual(tr1, tr2)

    def test_fingerprint(self):
        dic = {
            'date': '2020-03-03', 'par': 'ΤΔΑ3', 'per': 'Δοκιμή τεστ',
            'afm': '123123123',
            'lines': [
                {'account': '54.00.213', 'typ': 1, 'value': 13},
                {'account': '20.00.013', 'typ': 2, 'value': -100},
                {'account': '54.00.224', 'typ': 1, 'value': 24},
                {'account': '20.00.024', 'typ': 1, 'value': 100},
                {'account': '50.00.001', 'typ': 2, 'value': 237},
            ]
        }
        tr1 = Transaction.tran_from_dic(dic)
        # print(tr1.fingerprint)
        # print(tr1.account_pairs())
