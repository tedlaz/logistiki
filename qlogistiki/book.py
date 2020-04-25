# from collections import defaultdict
from decimal import Decimal
import qlogistiki.transaction as trs
from qlogistiki.utils import gr2strdec, account_levels
OUT, HEAD, LINE = 0, 1, 2
fpa_prefix = 'ΦΠΑ'


class Book:
    def __init__(self, afm, company_name):
        self.afm = afm
        self.company_name = company_name
        self.transactions = []

    @property
    def number_of_transactions(self):
        return len(self.transactions)

    def transactions_filter(self, apo=None, eos=None):
        for transaction in self.transactions:
            if apo and transaction.date < apo:
                continue
            if eos and transaction.date > eos:
                continue
            yield transaction

    def add_transaction(self, transaction):
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
                        f"{trn.date} {trn.perigrafi[:40]:40} "
                        f"{line.delta:>14} {rsum:>14}"
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

    def kartella_model(self, account):
        rsum = 0
        headers = ("Ημερομηνία", 'Παρ/κό', "Περιγραφή",
                   "Χρέωση", "Πίστωση", "Υπόλοιπο")
        align = (1, 1, 1, 3, 3, 3)
        typos = (0, 0, 0, 1, 1, 1)
        vals = []
        for trn in self.transactions:
            for line in trn.lines:
                laccount = line.account
                if trn.afm:
                    laccount = f"{line.account}.{trn.afm}"
                if laccount.startswith(account):
                    rsum += line.delta
                    if line.delta < 0:
                        xre = 0
                        pis = -line.delta
                    else:
                        xre = line.delta
                        pis = 0
                    vals.append([trn.date, trn.parastatiko,
                                 trn.perigrafi, xre, pis, rsum])
        vals.reverse()
        return headers, vals, align, typos

    def isozygio(self, apo=None, eos=None):
        accounts = {}
        total = 0
        for trn in self.transactions_filter(apo, eos):
            for line in trn.lines:
                accs = account_levels(line.account)
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

    def isozygio_afm(self, apo=None, eos=None):
        accounts = {}
        total = 0
        for trn in self.transactions_filter(apo, eos):
            for line in trn.lines:
                laccount = line.account
                if trn.afm:
                    laccount = f"{line.account}.{trn.afm}"
                accs = account_levels(laccount)
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
                    laccount = f"{line.account}.{trn.afm}"
                accs = account_levels(laccount)
                for acc in accs:
                    accounts[acc] = accounts.get(acc, 0)
                    accounts[acc] += line.delta
        return accounts

    def isozygio_model(self):
        lmoi = self.isozygio_delta()
        headers = ("Λογαριασμοί", "Υπόλοιπο")
        align = (1, 3)
        typos = (0, 1)
        vals = []
        for lmo in sorted(lmoi.keys()):
            vals.append((lmo, lmoi[lmo]))
        return headers, vals, align, typos

    def myf(self, apo, eos):
        pass

    def ee_book(self, apo, eos):
        pass

    def fpa(self, apo, eos):
        pass

    def fpa_status(self):
        for tran in self.transactions:
            if tran.fpa_status == 2:
                print(tran)

    def isologismos(self, apo, eos):
        pass

    def parse(self, file):
        status = OUT
        trn = None
        lines = []
        with open(file) as fil:
            lines = fil.read().split('\n')
        for line in lines:

            # Αγνόησε τις γραμμές σχολίων
            if line[:0] == '#':
                continue

            # Αγνόησε τις γραμμές με μέγεθος μικρότερο από 3
            if len(line.strip()) < 4:
                if status == LINE:
                    self.add_transaction(trn)
                status = OUT
                continue

            if line[:10].replace('-', '').isnumeric():  # Γραμμή Head
                if status == LINE:
                    self.add_transaction(trn)
                status = HEAD
                dat, par, _, per, *afma = line.split('"')
                dat = dat.strip()
                par = par.strip()
                per = per.strip()
                afm = afma[0].strip() if afma else ''
                trn = trs.Transaction(dat, par, per, afm)
            else:
                status = LINE
                account, *val = line.split()
                if account == fpa_prefix:
                    account = f'{fpa_prefix}.{trn.last_account}'
                    pfpa = Decimal(trn.last_account.split('.')[-1][3:][:-1])
                    calfpa = trn.last_delta * pfpa / Decimal(100)
                    trn.fpa_status = 1
                    if abs(Decimal(gr2strdec(val[0])) - calfpa) > 0.01:
                        trn.fpa_status = 2
                if val:
                    trn.add_line_delta(account, gr2strdec(val[0]))
                else:
                    trn.add_last_line(account)
        if status == LINE:
            self.add_transaction(trn)

    def __repr__(self) -> str:
        return (
            "Book("
            f"afm={self.afm!r}, "
            f"company={self.company_name!r}, "
            f"NumberOfTransactions={self.number_of_transactions}"
            ")"
        )
