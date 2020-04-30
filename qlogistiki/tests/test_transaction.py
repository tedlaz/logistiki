from unittest import TestCase
import qlogistiki.transaction as trn


class TestTransaction(TestCase):
    def test_transaction_line(self):
        lin = trn.TransactionLine('Αγορές.Εμπορευματων.18%', -15, 100)
        # print(lin, lin.__dict__)

    def test_new_from_delta(self):
        li1 = trn.TransactionLine.new_from_delta("Ταμείο", -100)
        li2 = trn.TransactionLine.new_from_delta("Ταμείο", 35)

    def test_transaction_01(self):
        tr1 = trn.Transaction('2020-01-10', '', 'Σουπερμαρκετ πόπη')
        tr1.add_line_delta('agores 24%', 100)
        tr1.add_line_delta('fpa 24%', 24)
        tr1.add_last_line('promitheftes')
        # print('\n', tr1.as_str())
        self.assertEqual(tr1.uid, '2020011012400')
        tr1.afm = '123123123'
        self.assertEqual(tr1.uid, '2020011012312312312400')
