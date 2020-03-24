import datetime as dtm
from collections import namedtuple
from enum import Enum
from typing import List, Type, TypeVar
from hashlib import sha1
from logistiki.tline import Tline
TTran = TypeVar("TTran", bound="Tran")
TBook = TypeVar("TBook", bound="Book")
TranTotals = namedtuple('TranTotals', 'tdebit tcredit delta')
EET = ['1.Esoda', '2.Agores', '2.Ejoda', '3.Pagia', '4.FPA']


class EE(Enum):
    esoda = 1
    agores = 2
    ejoda = 3
    pagia = 4
    fpa = 5
    loipa = 6


def account_tag(account: str) -> EE:
    if account.startswith('54.00'):
        return EE.fpa
    if account.startswith('1'):
        return EE.pagia
    if account.startswith('2'):
        return EE.agores
    if account.startswith('6'):
        return EE.ejoda
    if account.startswith('7'):
        return EE.esoda
    return EE.loipa


def account_cat(acc: str) -> tuple:
    if acc.startswith('54.00'):
        return ('54.00', 1)
    if acc.startswith('7'):
        return ('7', -1)
    return (acc[0], 1)


class Tran:
    """Transaction class containing header and Trand lines"""

    def __init__(self, isodate: str, par: str, per: str,
                 afm: str = '', _id: int = 0) -> None:
        self.id = _id
        self.date = dtm.date.fromisoformat(isodate)
        self.par = par
        self.per = per
        self.afm = afm
        self.lines: List[Tline] = []

    @classmethod
    def tran_from_dic(cls: Type[TTran], tran_dic: dict) -> TTran:
        new_tran = cls(tran_dic['date'], tran_dic['par'], tran_dic['per'])
        for lin in tran_dic['lines']:
            new_tran.add_line(lin['account'], lin['typ'], lin['value'])
        if 'id' in tran_dic:
            new_tran.id = tran_dic['id']
        new_tran.id = tran_dic.get('id', None)
        return new_tran

    @property
    def tags(self):
        ltag = list(set([i.tag.name for i in self.lines]))
        ltag.sort()
        return '_'.join(ltag)

    @property
    def size(self) -> int:
        return len(self.lines)

    @property
    def to_dict(self) -> dict:
        if not self.is_balanced:
            raise ValueError(f'Transaction {self}')
        adi = {
            'date': self.date.isoformat(),
            'par': self.par,
            'per': self.per,
            'lines': [line.to_dict for line in self.lines],
            'sha1': self.sha1
        }
        return adi

    @property
    def totals(self) -> TranTotals:
        tdebit = tcredit = 0.0
        for lin in self.lines:
            if lin.typ == 1:
                tdebit += lin.value
            else:
                tcredit += lin.value
        return TranTotals(tdebit, tcredit, tdebit - tcredit)

    @property
    def is_balanced(self) -> bool:
        if self.totals.delta != 0:
            return False
        if self.size < 2:
            return False
        return True

    def add_line(self, account: str, typ: int, value: float) -> None:
        self.lines.append(Tline(account, typ, value))

    def add_final(self, account: str) -> None:
        """Add final line and make sure transaction is balanced"""
        deb, cred, delta = self.totals
        if self.size == 0:
            return
        if delta == 0:
            return
        elif delta > 0:
            self.add_line(account, 2, delta)
        self.add_line(account, 1, -delta)

    @property
    def sha1(self) -> str:
        """Create sha1 of the class according to self._str_byte"""
        ash1 = sha1()
        ash1.update(self._str_byte)
        return ash1.hexdigest()

    @property
    def _str_byte(self) -> bytes:
        """String representation of Tran transformed to bytes"""
        ast = f"{self.date.isoformat()}{self.par}"
        for lin in self.lines:
            ast += f"{lin.account}{lin.typ}{lin.value}"
        return ast.encode()

    def __eq__(self, other: object) -> bool:
        """Overrides the default implementation"""
        if not isinstance(other, Tran):
            return NotImplemented
        return self.sha1 == other.sha1

    def __str__(self):
        is_balanced = ''
        if not self.is_balanced:
            is_balanced = f'(Not balanced){self.totals.delta}'
        st1 = '\n/-------|Transaction|---------------------------------\\\n'
        st1 += f"|  {self.tags}\n"
        st1 += f"|  {self.sha1}\n"
        st1 += f"|  {self.date} {self.par} {self.per} {is_balanced}\n"
        st1 += '\n'.join(['|  ' + i.__str__() for i in self.lines])
        st1 += '\n\\-----------------------------------------------------/\n'
        return st1


class Book:
    def __init__(self, name: str) -> None:
        self.name = name
        self._accounts = set()
        self.trans: List[Tran] = []

    @classmethod
    def book_from_list(cls: Type[TBook], name, tran_list: list) -> TBook:
        book = cls(name)
        for tran in tran_list:
            book.add(Tran.tran_from_dic(tran))
        return book

    @property
    def to_list(self) -> list:
        lst = []
        for trn in self.trans:
            lst.append(trn.to_dict)
        return lst

    def add(self, tran: Tran) -> None:
        for lin in tran.lines:
            self._accounts.add(lin.account)
        self.trans.append(tran)

    @property
    def accounts(self):
        return sorted(self._accounts)

    def __str__(self) -> str:
        ttt = f"Book {self.name}"
        for tran in self.trans:
            ttt += tran.__str__()
        return ttt


if __name__ == '__main__':
    # import parser
    # bbo = Book.book_from_list('test', parser.read_file('katax.xlsx'))
    # print(bbo)
    a = Tline('20.00', 2, 10)
    b = Tline('20.0', 1, 5)
    print(Tline('20', 1, 0) + a + b)
    print(b.flat_value)
