from collections import namedtuple, defaultdict
from decimal import Decimal
from qlogistiki.dec import Dec
from qlogistiki.account import Account
from qlogistiki.transaction_line import TransactionLine

DEBIT, CREDIT = 1, 2
decr = {1: 'Χρέωση', 2: 'Πίστωση'}
# 0: Χωρίς ΦΠΑ, 1: ΦΠΑ οκ, 2: ΦΠΑ λάθος
NOFPA, FPAOK, FPAERROR = 0, 1, 2
fpastatus = {0: 'Χωρίς ΦΠΑ', 1: 'ΦΠΑ οκ', 2: 'ΦΠΑ λάθος'}
Trl = namedtuple('Trl', 'date par per afm acc typos val')


class Transaction:
    cid = 0
    __slots__ = ['id', 'date', 'parastatiko', 'perigrafi',
                 'afm', 'delta', 'lines', 'fpa_status']

    def __init__(self, date: str, parastatiko: str, perigrafi: str, afm=''):
        self.__class__.cid += 1
        self.id = self.cid
        self.date = date
        self.parastatiko = parastatiko
        self.perigrafi = perigrafi
        self.afm = afm
        self.delta = Dec(0)
        self.lines = []
        self.fpa_status = 0  # 0: Χωρίς ΦΠΑ, 1: ΦΠΑ οκ, 2: ΦΠΑ λάθος

    def lines_full(self):
        full_lines = [
            Trl(self.date, self.parastatiko, self.perigrafi,
                self.afm, l.account, l.typos, l.value) for l in self.lines
        ]
        return full_lines

    @property
    def uid(self) -> str:
        date_part = self.date.replace('-', '')
        afm_part = self.afm  # or '000000000'
        parastatiko_part = self.parastatiko.replace(' ', '')
        val_part = self.total.uid
        return f'{date_part}{afm_part}{parastatiko_part}{val_part}'

    @property
    def number_of_lines(self) -> int:
        return len(self.lines)

    @property
    def is_balanced(self) -> bool:
        if self.number_of_lines < 2:
            return False
        if self.delta == 0:
            return True
        return False

    @property
    def total(self) -> Dec:
        return sum(l.debit for l in self.lines)

    def add_line(self, account: str, value):
        new_line = TransactionLine(account, value)
        self.lines.append(new_line)
        self.delta += new_line.delta

    def add_connected_lines(self, acc1, acc2, value, pososto):
        self.add_line(acc1, value)
        self.add_line(acc2, value * pososto / 100)

    def add_last_line(self, account):
        if self.delta == 0:
            raise ValueError(f'Transaction {self} is already balanced')
        new_line = TransactionLine(account, -self.delta)
        self.lines.append(new_line)

    @property
    def last_account(self) -> Account:
        if self.number_of_lines == 0:
            raise ValueError('Impossible value')
        return self.lines[-1].account

    @property
    def last_delta(self):
        if self.number_of_lines == 0:
            return 0
        return self.lines[-1].delta

    def __repr__(self) -> str:
        lins = ','.join([repr(lin) for lin in self.lines])
        return (
            "Transaction("
            f"date={self.date!r}, "
            f"parastatiko={self.parastatiko!r}, "
            f"perigrafi={self.perigrafi!r}, "
            f"afm={self.afm!r}, "
            f"fpa_status={fpastatus[self.fpa_status]!r}, "
            f"lines=[{lins}]"
            ")"
        )

    def as_str(self):
        maxnam = max([len(i.account.name) for i in self.lines])
        stt = f'{self.date} "{self.parastatiko}" "{self.perigrafi}" {self.afm}\n'
        for i, lin in enumerate(self.lines):
            if self.number_of_lines == i + 1:
                stt += f'  {lin.account.name}\n'
            else:
                tlin = f'  {lin.account.name:<{maxnam}} {lin.delta.gr0:>14}'
                stt += tlin.rstrip() + '\n'
        return stt

    def __str__(self) -> str:
        ast = f'\n{self.date} {self.parastatiko} {self.perigrafi} {self.afm}\n'
        for lin in self.lines:
            ast += f'{lin.account.name:<40}{lin.debit:>14}{lin.credit:>14}\n'
        return ast

    def __eq__(self, oth):
        return self.date == oth.date and self.parastatiko == oth.parastatiko

    def __lt__(self, oth):
        if self.date == oth.date:
            return self.total < oth.total
        return self.date < oth.date
