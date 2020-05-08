from collections import namedtuple, defaultdict
from decimal import Decimal
from qlogistiki.utils import dec, gr_num

DEBIT, CREDIT = 1, 2
decr = {1: 'Χρέωση', 2: 'Πίστωση'}
# 0: Χωρίς ΦΠΑ, 1: ΦΠΑ οκ, 2: ΦΠΑ λάθος
NOFPA, FPAOK, FPAERROR = 0, 1, 2
fpastatus = {0: 'Χωρίς ΦΠΑ', 1: 'ΦΠΑ οκ', 2: 'ΦΠΑ λάθος'}
Trl = namedtuple('Trl', 'date par per afm acc typos val')


class AccountList(list):
    @property
    def names(self):
        return [a.name for a in self]

    @property
    def full_tree(self):
        stree = set()
        for account in self:
            for lmo in account.tree:
                stree.add(lmo)
        ltree = list(stree)
        ltree.sort()
        return ltree


class Account():
    splitter = '.'
    # account_list = AccountList()
    # account_dict = defaultdict(Decimal)
    __slots__ = ['name', ]

    def __init__(self, name):
        self.name = name
        # if self.name not in self.account_list.names:
        #     Account.account_list.append(self)

    @property
    def tree(self):
        spl = self.name.split(self.splitter)
        lvls = [self.splitter.join(spl[: i + 1]) for i, _ in enumerate(spl)]
        return lvls

    @property
    def tree_reversed(self):
        lvls = self.tree
        lvls.reverse()
        return lvls

    def __repr__(self):
        return f'Account(name={self.name!r})'


class TransactionLine:
    __slots__ = ['account', 'typos', 'value']

    def __init__(self, account, typos, value):
        self.account = Account(account)
        if typos <= 1:
            self.typos = 1
        else:
            self.typos = 2
        self.value = dec(value)
        self.normalize()
        # Account.account_dict[account] += self.delta

    def normalize(self):
        if self.value < 0:
            if self.typos == DEBIT:
                self.typos = CREDIT
            else:
                self.typos = CREDIT
            self.value = -self.value

    @classmethod
    def new_from_delta(cls, account, delta):
        return cls(Account(account), 1, delta)

    @property
    def debit(self):
        if self.typos == 1:
            return self.value
        return dec(0)

    @property
    def credit(self):
        if self.typos == 2:
            return self.value
        return dec(0)

    @property
    def delta(self):
        if self.typos == 1:
            return self.value
        return -self.value

    def __eq__(self, other):
        return self.delta == other.delta

    def __lt__(self, other):
        return self.delta < other.delta

    def __add__(self, other):
        if self.account.name != other.account.name:
            raise ValueError('For addition accounts must me the same')
        return TransactionLine.new_from_delta(
            self.account.name, self.delta + other.delta
        )

    def __repr__(self):
        return (
            "TransactionLine("
            f"account={self.account!r}, "
            f"typos={decr[self.typos]!r}, "
            f"value={self.value!r}"
            ")"
        )


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
        self.delta = dec(0)
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
        val_part = str(self.total).replace('.', '')
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
    def total(self):
        return sum(l.debit for l in self.lines)

    def add_line(self, account: str, typos: int, value):
        new_line = TransactionLine(account, typos, value)
        self.lines.append(new_line)
        self.delta += new_line.delta

    def add_line_delta(self, account, value):
        value = dec(value)
        if value < 0:
            self.add_line(account, 2, -value)
        else:
            self.add_line(account, 1, value)

    def add_connected_lines(self, acc1, acc2, value, pososto):
        self.add_line_delta(acc1, value)
        self.add_line_delta(acc2, dec(value * dec(pososto) / dec(100)))

    def add_last_line(self, account):
        if self.delta == 0:
            raise ValueError(f'Transaction {self} is already balanced')
        if self.delta < 0:
            new_line = TransactionLine(account, 1, -self.delta)
        else:
            new_line = TransactionLine(account, 2, self.delta)
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
        stt = f'{self.date} "{self.parastatiko}" "{self.perigrafi}" {self.afm}\n'
        for i, lin in enumerate(self.lines):
            if self.number_of_lines == i + 1:
                stt += f'  {lin.account.name}\n'
            else:
                tlin = f'  {lin.account.name:<40} {gr_num(lin.delta):>14}'
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
