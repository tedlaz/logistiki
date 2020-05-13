from collections import namedtuple
from dataclasses import dataclass
import os
# from decimal import Decimal
import qlogistiki.transaction as trs
from qlogistiki.utils import gr2strdec, account_tree, gr2dec
OUT, HEAD, LINE = 0, 1, 2
fpa_prefix = 'ΦΠΑ'
ValPoint = namedtuple('ValPoint', 'date account delta')


@dataclass
class ModelValues:
    """Use it to pass values to qt models
    headers : headers for fields
    aligns  : aligment for fields (1=left, 2=center, 3=right)
    types   : types for fields (0=text, 1=numeric)
    sizes   : gird width for fields
    values  : list of records
    """
    headers: tuple
    aligns: tuple
    types: tuple
    sizes: tuple
    values: list


class Book:
    __slots__ = ['afm', 'company_name',
                 'transactions', 'validations', 'accounts']

    def __init__(self, afm, company, trans: list, vals, accounts):
        self.afm = afm
        self.company_name = company
        self.transactions = trans
        self.validations = vals
        self.accounts = accounts

    def validate(self):
        errors = []
        correct_checks = 0
        for vpoint in self.validations:
            ypol = self.ypoloipo(vpoint.account, vpoint.date)
            diafora = ypol - vpoint.delta
            if diafora == 0:
                correct_checks += 1
            else:
                errors.append(
                    f'{vpoint.date}: {vpoint.account:30} {ypol:>14}-> {diafora}')
        return correct_checks, errors

    def max_account_name(self):
        if self.accounts:
            return max([len(i) for i in self.accounts.keys()])
        return 0

    @property
    def number_of_transactions(self):
        if self.transactions:
            return len(self.transactions)
        return 0

    def transactions_filter(self, apo=None, eos=None):
        for transaction in self.transactions:
            if apo and transaction.date < apo:
                continue
            if eos and transaction.date > eos:
                continue
            yield transaction

    def add_transaction(self, transaction):
        if not self.transactions:
            self.transactions = []
        if isinstance(transaction, trs.Transaction):
            self.transactions.append(transaction)
        else:
            raise ValueError(f"{transaction} is not a Transaction object")

    def kartella(self, account, apo=None, eos=None):
        rsum = 0
        for trn in self.transactions_filter(apo, eos):
            for line in trn.lines:
                if line.account.startswith(account):
                    rsum += line.delta
                    print(
                        f"{trn.date} {line.account:30} {trn.parastatiko:20} "
                        f"{trn.perigrafi[:40]:40} {line.delta:>14} {rsum:>14}"
                    )

    def kartella_afm(self, account, apo=None, eos=None):
        rsum = 0
        for trn in self.transactions_filter(apo, eos):
            for line in trn.lines:
                laccount = line.account
                if trn.afm:
                    laccount = f"{line.account}.{trn.afm}"
                if laccount.startswith(account):
                    rsum += line.delta
                    print(
                        f"{trn.date} {trn.perigrafi[:40]:40} "
                        f"{line.delta:>14} {rsum:>14}"
                    )

    def kartella_model(self, account: str, max_vals=200) -> ModelValues:
        rsum = 0
        headers = ('id', "Ημερομηνία", 'Παρ/κό', "Περιγραφή",
                   "Χρέωση", "Πίστωση", "Υπόλοιπο")
        align = (0, 1, 1, 1, 3, 3, 3)
        typos = (0, 0, 0, 0, 1, 1, 1)
        sizes = (50, 90, 80, 400, 80, 80, 80)
        vals = []
        for trn in sorted(self.transactions):
            for line in trn.lines:
                laccount = line.account.name
                if trn.afm:
                    laccount = f"{line.account.name}.{trn.afm}"
                if laccount.startswith(account):
                    rsum += line.delta
                    if line.delta < 0:
                        xre = 0
                        pis = -line.delta
                    else:
                        xre = line.delta
                        pis = 0
                    vals.append([trn.id, trn.date, trn.parastatiko,
                                 trn.perigrafi, xre, pis, rsum])
        vals.reverse()
        return ModelValues(headers, align, typos, sizes, vals[:max_vals])

    def ypoloipo(self, account, eos=None):
        ypol = 0
        for trn in self.transactions_filter(None, eos):
            for line in trn.lines:
                if line.account.name.startswith(account):
                    ypol += line.delta
        return ypol

    def isozygio(self, apo=None, eos=None):
        accounts = {}
        total = 0
        for trn in self.transactions_filter(apo, eos):
            for line in trn.lines:
                acc = line.account.name
                accounts[acc] = accounts.get(acc, [0, 0])
                accounts[acc][0] += line.debit
                accounts[acc][1] += line.credit
                total += line.delta
        for key in sorted(accounts):
            delta = accounts[key][0] - accounts[key][1]
            print(
                f"{key:<50} {accounts[key][0]:>14} "
                f"{accounts[key][1]:>14} {delta:>14}"
            )
        print(f"{'Σύνολο':^50} {total:>14}")

    def isozygio_afm(self, apo=None, eos=None):
        accounts = {}
        total = 0
        for trn in self.transactions_filter(apo, eos):
            for line in trn.lines:
                laccount = line.account.name
                if trn.afm:
                    laccount = f"{line.account.name}.{trn.afm}"
                accs = account_tree(laccount)
                for acc in accs:
                    accounts[acc] = accounts.get(acc, [0, 0])
                    accounts[acc][0] += line.debit
                    accounts[acc][1] += line.credit
                total += line.delta
        for key in sorted(accounts):
            delta = accounts[key][0] - accounts[key][1]
            print(
                f"{key:<50} {accounts[key][0]:>14} "
                f"{accounts[key][1]:>14} {delta:>14}"
            )
        print(f"{'Σύνολο':^50} {total:>14}")

    def isozygio_delta(self):
        accounts = {}
        for trn in self.transactions:
            for line in trn.lines:
                laccount = line.account
                if trn.afm:
                    laccount = trs.Account(f"{line.account.name}.{trn.afm}")
                for acc in laccount.tree:
                    accounts[acc] = accounts.get(acc, 0)
                    accounts[acc] += line.delta
        return accounts

    def isozygio_model(self) -> ModelValues:
        # print(self.check_uid())
        lmoi = self.isozygio_delta()
        headers = ("Λογαριασμοί", "Υπόλοιπο")
        align = (1, 3)
        typos = (0, 1)
        sizes = (200, 100)
        vals = []
        for lmo in sorted(lmoi.keys()):
            vals.append((lmo, lmoi[lmo]))
        return ModelValues(headers, align, typos, sizes, vals)

    def check_uid(self):
        uid_set = set()
        for trn in self.transactions:
            uid = trn.uid
            if uid in uid_set:
                print(trn)
            uid_set.add(trn.uid)
        return len(uid_set), self.number_of_transactions

    def myf(self, apo, eos):
        pass

    def ee_book(self, apo, eos):
        pass

    def fpa(self, apo, eos):
        pass

    def fpa_status(self):
        fpa_errors = []
        for tran in self.transactions:
            # 0: Χωρίς ΦΠΑ, 1: ΦΠΑ οκ, 2: ΦΠΑ λάθος
            if tran.fpa_status == 2:
                fpa_errors.append(tran)
        if fpa_errors:
            print('Υπάρχουν λάθη σε εγγραφές ΦΠΑ')
            print('\n'.join(fpa_errors))
        else:
            print("Δεν υπάρχουν λάθη σε εγγραφές με ΦΠΑ")

    def isologismos(self, apo, eos):
        pass

    def __repr__(self) -> str:
        return (
            "Book("
            f"afm={self.afm!r}, "
            f"company={self.company_name!r}, "
            f"NumberOfTransactions={self.number_of_transactions}"
            ")"
        )
