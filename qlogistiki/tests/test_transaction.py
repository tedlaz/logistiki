from unittest import TestCase
import qlogistiki.transaction as trn


class TestTransaction(TestCase):
    def test_transaction_line(self):
        lin = trn.TransactionLine('Αγορές.Εμπορευματων.18%', -15, 100)
        print(lin, lin.debit, lin.credit, lin.delta)
