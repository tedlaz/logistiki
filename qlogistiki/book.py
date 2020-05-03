# from collections import defaultdict
import os
from decimal import Decimal
import qlogistiki.transaction as trs
from qlogistiki.utils import gr2strdec, account_tree
OUT, HEAD, LINE = 0, 1, 2
fpa_prefix = 'ΦΠΑ'


class ModelValues:
    """Use it to pass values to qt models"""

    def __init__(self, headers, aligns, types, sizes, values):
        """
        heades : headers for fields
        aligns : aligment for fields (1=left, 2=center, 3=right)
        types  : types for fields (0=text, 1=numeric)
        sizes  : gird width for fields
        values : list of records
        """
        self.headers = headers
        self.aligns = aligns
        self.types = types
        self.sizes = sizes
        self.values = values


class Book:
    def __init__(self, afm, company_name):
        self.afm = afm
        self.company_name = company_name
        self.transactions = []
        self.account_tree = []

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

    def kartella_model(self, account: str) -> ModelValues:
        rsum = 0
        headers = ('id', "Ημερομηνία", 'Παρ/κό', "Περιγραφή",
                   "Χρέωση", "Πίστωση", "Υπόλοιπο")
        align = (0, 1, 1, 1, 3, 3, 3)
        typos = (0, 0, 0, 0, 1, 1, 1)
        sizes = (50, 90, 80, 400, 80, 80, 80)
        vals = []
        for trn in self.transactions:
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
        return ModelValues(headers, align, typos, sizes, vals)

    def isozygio(self, apo=None, eos=None):
        accounts = {}
        total = 0
        for trn in self.transactions_filter(apo, eos):
            for line in trn.lines:
                for acc in line.account.tree:
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
                laccount = line.account.name
                if trn.afm:
                    laccount = f"{line.account.name}.{trn.afm}"
                accs = account_tree(laccount)
                for acc in accs:
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

    def parse(self, file):
        status = OUT
        trn = None
        lines = []
        with open(file) as fil:
            lines = fil.read().split('\n')
        for line in lines:
            rline = line.rstrip()
            # Αγνόησε τις γραμμές σχολίων
            if rline.startswith('#'):
                continue

            # Αγνόησε τις γραμμές με μέγεθος μικρότερο από 3
            elif len(rline) == 0:
                if status == LINE:
                    self.add_transaction(trn)
                status = OUT
                continue

            elif rline[:10].replace('-', '').isnumeric():  # Γραμμή Head
                if status == LINE:
                    self.add_transaction(trn)
                status = HEAD
                dat, par, _, per, *afma = rline.split('"')
                dat = dat.strip()
                par = par.strip()
                per = per.strip()
                afm = afma[0].strip() if afma else ''
                trn = trs.Transaction(dat, par, per, afm)
            else:
                status = LINE
                account, *val = rline.split()
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
            status = OUT
        self.account_tree = trs.Account.account_list.full_tree

    def write2file(self, filename):
        if os.path.exists(filename):
            raise ValueError('file already exists')
        with open(filename, 'w') as fil:
            for trn in self.transactions:
                fil.write(trn.as_str())
                fil.write('\n')

    def __repr__(self) -> str:
        return (
            "Book("
            f"afm={self.afm!r}, "
            f"company={self.company_name!r}, "
            f"NumberOfTransactions={self.number_of_transactions}"
            ")"
        )
