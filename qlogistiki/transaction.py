"""Module Transaction"""
from collections import namedtuple
from .dec import Dec
from .account import Account
from .transaction_line import TransactionLine

DEBIT, CREDIT = 1, 2
decr = {1: "Χρέωση", 2: "Πίστωση"}
# 0: Χωρίς ΦΠΑ, 1: ΦΠΑ οκ, 2: ΦΠΑ λάθος
NOFPA, FPAOK, FPAERROR = 0, 1, 2
fpastatus = {0: "Χωρίς ΦΠΑ", 1: "ΦΠΑ οκ", 2: "ΦΠΑ λάθος"}
Trl = namedtuple("Trl", "date par per afm acc typos val")


class Transaction:
    """
    Class dealing with transactions
    """

    cid = 0
    __slots__ = [
        "id",
        "date",
        "parastatiko",
        "perigrafi",
        "afm",
        "delta",
        "lines",
        "fpa_status",
    ]

    def __init__(self, date: str, parastatiko: str, perigrafi: str, afm=""):
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
        """Transaction lines enriched with date, parastatiko, per, afm"""
        full_lines = [
            Trl(
                self.date,
                self.parastatiko,
                self.perigrafi,
                self.afm,
                l.account,
                l.typos,
                l.value,
            )
            for l in self.lines
        ]
        return full_lines

    @property
    def uid(self) -> str:
        """
        Generate a unique id
        """
        date_part = self.date.replace("-", "")
        afm_part = self.afm  # or '000000000'
        parastatiko_part = self.parastatiko.replace(" ", "")
        val_part = str(self.total).replace(',', '')
        return f"{date_part}{afm_part}{parastatiko_part}{val_part}"

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

    def get_lines_by_account(self, account_part, running_sum, found):
        """
            If a transaction has more than one lines according to account_part
            group them together as one with theyr sum as value
        """
        for line in self.lines:
            if line.account.name.startswith(account_part):
                if line.sxolio:
                    per = self.perigrafi + ", " + line.sxolio
                else:
                    per = self.perigrafi
                running_sum["total"] += line.value
                found.append(
                    (
                        self.id,
                        self.date,
                        self.parastatiko,
                        per,
                        line.debit,
                        line.credit,
                        running_sum["total"],
                    )
                )

    def add_line(self, account: str, value, sxolio=""):
        new_line = TransactionLine(account, value, sxolio)
        self.lines.append(new_line)
        self.delta += new_line.delta

    def add_connected_lines(self, acc1, acc2, value, pososto):
        self.add_line(acc1, value)
        self.add_line(acc2, value * pososto / 100.0)

    def add_last_line(self, account, sxolio=""):
        if self.delta == 0:
            raise ValueError(f"Transaction {self} is already balanced")
        new_line = TransactionLine(account, -self.delta, sxolio)
        self.lines.append(new_line)

    @property
    def last_account(self) -> Account:
        if self.number_of_lines == 0:
            raise ValueError("Impossible value")
        return self.lines[-1].account

    @property
    def last_delta(self):
        if self.number_of_lines == 0:
            return 0
        return self.lines[-1].delta

    def __repr__(self) -> str:
        lins = ",".join([repr(lin) for lin in self.lines])
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
        """returns a string representation of transaction"""
        maxnam = max([len(i.account.name) for i in self.lines])
        maxn = max([len(i.delta.gr0) for i in self.lines])
        if self.afm:
            stt = f'{self.date} "{self.parastatiko}" "{self.perigrafi}" {self.afm}\n'
        else:
            stt = f'{self.date} "{self.parastatiko}" "{self.perigrafi}"\n'
        for i, lin in enumerate(self.lines):
            if self.number_of_lines == i + 1:
                stt += f"  {lin.account.name}\n"
            else:
                if lin.sxolio:
                    tlin = f"  {lin.account.name:<{maxnam}} {lin.delta.gr0:>{maxn}} # {lin.sxolio}"
                else:
                    tlin = f"  {lin.account.name:<{maxnam}} {lin.delta.gr0:>{maxn}}"
                stt += tlin.rstrip() + "\n"
        return stt

    def __str__(self) -> str:
        ast = f"\n{self.date} {self.parastatiko} {self.perigrafi} {self.afm}\n"
        for lin in self.lines:
            ast += f"  {lin}\n"
        return ast

    def __eq__(self, oth):
        return self.date == oth.date and self.parastatiko == oth.parastatiko

    def __lt__(self, oth):
        if self.date == oth.date:
            return self.id < oth.id
        return self.date < oth.date
