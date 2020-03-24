import datetime as dtm
from decimal import Decimal
from hashlib import sha1
from collections import namedtuple, defaultdict
from typing import List, Type, TypeVar, ValuesView
from logistiki.transaction_line import TransactionLine
from logistiki.udec import dec

TranTotals = namedtuple('TranTotals', 'tdebit tcredit delta counter')
Myf = namedtuple('Myf', 'typ xrpi date par val fpa tot')
Ee = namedtuple('Ee', 'typ xrpi date ptyp par val fpa tot')
TTran = TypeVar("TTran", bound="Transaction")


def difference(acc1, acc2):
    acc1 = acc1.replace('.', '')
    acc2 = acc2.replace('.', '')
    if acc1.startswith('5400'):
        acc1 = acc1[4:]
    if acc2.startswith('5400'):
        acc2 = acc2[4:]
    if acc1 == acc2:
        return 0
    score = 0
    if acc1[-2:] != acc2[-2:]:
        score += 100
    for el in acc1:
        if el not in acc2:
            score += 10
    for el in acc2:
        if el not in acc1:
            score += 10
    return score


class Transaction:
    """
    Transaction class containing header and Trand lines
    """

    def __init__(self, isodate: str, par: str, per: str,
                 afm: str = '', _id: int = 0) -> None:
        self.id = _id
        self.date = dtm.date.fromisoformat(isodate)
        self.par = par
        self.per = per
        self.afm = afm
        self.lines: List[TransactionLine] = []

    @classmethod
    def tran_from_dic(cls: Type[TTran], tran_dic: dict) -> TTran:
        """
        tran_dic : {
            'date': 'YYYY-MM-DD', 'par': 'ΤΔΑ1', 'per': 'Δοκιμή'
        }
        """
        new_tran = cls(tran_dic['date'], tran_dic['par'], tran_dic['per'])
        new_tran.afm = tran_dic.get('afm', '')
        new_tran.id = tran_dic.get('id', 0)
        for lin in tran_dic['lines']:
            new_tran.add_line(lin['account'], lin['typ'], lin['value'])
        return new_tran

    @classmethod
    def tran_from_ntuple(cls: Type[TTran], ntuple) -> TTran:
        new_tran = cls(ntuple.date, ntuple.parastatiko, ntuple.perigrafi,
                       '', ntuple.id)
        for lin in ntuple.lines:
            new_tran.add_line(lin.account, lin.typ, lin.value)
        return new_tran

    @property
    def new_object(self):
        new_tran = Transaction(
            self.date.isoformat(), self.par, self.per, self.afm, self.id
        )
        for lin in self.lines:
            new_tran.add_line_object(lin.new_object)
        return new_tran

    @property
    def new_normal(self):
        """
        Returns a new normalized Transaction object
        """
        new_tran = Transaction(
            self.date.isoformat(), self.par, self.per, self.afm, self.id
        )
        for lin in self.lines:
            new_tran.add_line_object(lin.new_normal)
        return new_tran

    @property
    def new_negative(self):
        """
        Returns a new negative Transtaction object
        (Exactly the same object with oposite signs)
        """
        new_tran = Transaction(
            self.date.isoformat(), self.par, self.per, self.afm, self.id
        )
        for lin in self.lines:
            new_tran.add_line_object(lin.new_negative)
        return new_tran

    @property
    def fingerprint(self):
        """
        fingerprint according to accounts
        """
        debs = set()
        crds = set()
        for lin in self.new_normal.lines:
            acc = lin.account.code
            if acc.startswith('54.00'):
                acc = '54.00' + '.' + acc[-2:]
            else:
                if acc[0] in '1267':
                    acc = acc[:2] + '.' + acc[-2:]
                else:
                    acc = acc[0]
            if lin.typ == 1:
                debs.add(acc)
            else:
                crds.add(acc)
        tdebs = ':'.join(sorted(list(debs)))
        tcrds = ':'.join(sorted(list(crds)))
        return f"{tdebs}<>{tcrds}"

    def myf(self):
        tval = tfpa = dec(0)
        ttyp = ''
        xrpi = ''
        isapo = False
        for lin in self.new_normal.lines:
            acc = lin.account.code
            if acc[0] in '126':
                if acc[:2] in ('60', '65', '66'):
                    continue
                isapo = True
                ttyp = 'ejoda'
                if lin.typ == 1:
                    xrpi = 'normal'
                else:
                    xrpi = 'credit'
                tval += lin.value
            elif acc.startswith('7'):
                isapo = True
                ttyp = 'esoda'
                if lin.typ == 2:
                    xrpi = 'normal'
                else:
                    xrpi = 'credit'
                tval += lin.value
            elif acc.startswith('54.00'):
                tfpa += lin.value
        return isapo, Myf(ttyp, xrpi, self.date.isoformat(),
                          self.par, tval, tfpa, tval + tfpa)

    def ee(self):
        tval = tfpa = dec(0)
        ttyp = xrpi = ''
        isee = False
        for lin in self.new_normal.lines:
            acc = lin.account.code
            if acc[0] in '126':
                isee = True
                ttyp = 'ejoda'
                if lin.typ == 1:
                    xrpi = 'normal'
                else:
                    xrpi = 'credit'
                tval += lin.value
            elif acc.startswith('7'):
                isee = True
                ttyp = 'esoda'
                if lin.typ == 2:
                    xrpi = 'normal'
                else:
                    xrpi = 'credit'
                tval += lin.value
            elif acc.startswith('54.00'):
                tfpa += lin.value
        ptyp, pno = self.par.split('--')
        # typ xrpi date ptyp par val fpa tot
        return isee, Ee(ttyp, xrpi, self.date.isoformat(),
                        ptyp, pno, tval, tfpa, tval + tfpa)

    def get_fpa_apot(self):
        """
        Χωρίζει τις γραμμές του άρθρου σε γραμμές ΦΠΑ και γραμμές
        αποτελεσματικές (1, 2, 6, 7)
        fpas = {'54.00.213': object_line, ...}
        apot = {'20.00.013': object_linea, '24.00.024': object_line2, ...}
        """
        fpas = {}
        apot = {}
        for lin in self.lines:
            acc = lin.account.code
            if acc.startswith('54.00'):
                if not acc.startswith('54.00.99'):
                    fpas[acc] = lin
            elif acc[0] in '1267':  # Για λόγους ΦΠΑ παίρνουμε και την ομάδα 6
                apot[acc] = lin
        if fpas:  # Αν υπάρχουν γραμμές ΦΠΑ τότε προχώρα
            return apot, fpas
        return None, None  # Διαφορετικά δώσε None

    def account_pairs(self):
        vats = set()
        apot = set()
        for lin in self.lines:
            acc = lin.account.code
            if acc.startswith('54.00'):
                if not acc.startswith('54.00.99'):
                    vats.add(acc)
            elif acc[0] in '1267':
                apot.add(acc)
        vats = list(vats)
        if vats == []:
            return []
        vats.sort()
        apot = list(apot)
        apot.sort()
        pairs = {}
        final = []
        for acc1 in vats:
            pairs[acc1] = {}
            for acc2 in apot:
                pairs[acc1][difference(acc1, acc2)] = acc2
        # print(pairs)
        for fpa in pairs:
            try:
                final.append((pairs[fpa][min(pairs[fpa])], fpa))
            except ValueError:
                print(pairs)
                return []
        # print(final)
        return final

    def __neg__(self):
        """
        returns a new revesed object
        """
        new_tran = Transaction(
            self.date.isoformat(), self.par, self.per, self.afm, self.id
        )
        for lin in self.lines:
            new_tran.add_line_object(-lin)
        return new_tran

    def normalize(self):
        """
        Normalizes current object
        """
        for line in self.lines:
            line.normalize()

    @property
    def typos(self):
        decre = {1: [], 2: []}
        omades = set()
        norm = self.new_normal
        for line in norm.lines:
            decre[line.typ].append(line)
            typos = line.account.typos
            typ = line.typ
            omades.add(int(f'{typos.value}{typ}'))
        # print(norm)
        # print(self)
        return sorted(list(omades))

    # @property
    # def tags(self):
    #     ltag = list(set([i.tag.name for i in self.lines]))
    #     ltag.sort()
    #     return '_'.join(ltag)

    @property
    def size(self) -> int:
        return len(self.lines)

    @property
    def to_ee(self):
        """
        Transform transaction to Esoda Ejoda type
        """
        vat_lines = []
        ee_lines = []
        for line in self.new_normal.lines:
            if line.account.is_fpa:
                vat_lines.append(line)
            else:
                if line.account.is_ee:
                    ee_lines.append(line)
        if len(vat_lines) > len(ee_lines):
            raise ValueError(f"FPA accounts must be less or equal than ee")
        return sum([i.value for i in ee_lines]), sum([i.value for i in vat_lines])

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
        tdebit = tcredit = 0
        for lin in self.lines:
            if lin.typ == 1:
                tdebit += lin.value
            else:
                tcredit += lin.value
        return TranTotals(tdebit, tcredit, tdebit - tcredit, len(self.lines))

    @property
    def is_balanced(self) -> bool:
        if self.totals.delta != 0:
            return False
        if self.size < 2:
            return False
        return True

    def add_line(self, account: str, typ: int, value) -> None:
        self.lines.append(TransactionLine.new_by_code(account, typ, value))

    def add_line_object(self, transaction_line_object):
        if not isinstance(transaction_line_object, TransactionLine):
            raise ValueError('Not a TransactionLine object')
        self.lines.append(transaction_line_object)

    def add_calculated(self, acc1, acc2, typ, value, percent):
        self.add_line(acc1, typ, value)
        self.add_line(acc2, typ, value * percent)

    def add_final(self, account: str) -> None:
        """Add final line and make sure transaction is balanced"""
        totals = self.totals
        if totals.counter == 0:
            raise ValueError(f"Transaction {self} is empty")
        if totals.delta == 0:
            return
        elif totals.delta > 0:
            if totals.tdebit == 0:
                self.add_line(account, 1, -totals.delta)
            else:
                self.add_line(account, 2, totals.delta)
        if totals.tcredit == 0:
            self.add_line(account, 2, totals.delta)
        else:
            self.add_line(account, 1, -totals.delta)

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

    def __str_for_comparison(self):
        return f"{self.date.isoformat()}{self.par}"

    def __add__(self, other) -> TTran:
        if not isinstance(other, Transaction):
            return NotImplemented
        date = self.date.isoformat()
        par = self.par
        per = self.per
        new = Transaction(date, par, per)
        dlines = defaultdict(Decimal)
        for lin in self.lines:
            dlines[lin.account.code] += lin.flat_value
        for lin in other.new_normal.lines:
            dlines[lin.account.code] += lin.flat_value
        for key, val in dlines.items():
            new.add_line(key, 1, val)
        new.normalize()
        return new

    def __mul__(self, anumber) -> TTran:
        fval = float(anumber)
        new_tran = Transaction(
            self.date.isoformat(), self.par, self.per, self.afm, self.id
        )
        for lin in self.lines:
            new_tran.add_line_object(lin * fval)
        return new_tran

    def __eq__(self, other: object) -> bool:
        """Overrides the default implementation"""
        if not isinstance(other, Transaction):
            return NotImplemented
        if self.date != other.date:
            return False
        if self.par != other.par:
            return False
        if self.per != other.per:
            return False
        if self.afm != other.afm:
            return False
        ls1 = sorted(self.lines)
        ls2 = sorted(other.lines)
        if len(ls1) != len(ls2):
            return False
        for i, acc_lin in enumerate(ls1):
            if not (acc_lin == ls2[i]):
                return False
        return True

    def __repr__(self):
        return (
            f"Transaction(date='{self.date.isoformat()}', "
            f"par='{self.par}', per='{self.per}', afm='{self.afm}', "
            f"id='{self.id}', lines={self.lines})"
        )

    def __lt__(self, other):
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.__str_for_comparison() < other.__str_for_comparison()

    def __str__(self):
        is_balanced = ''
        if not self.is_balanced:
            is_balanced = f'(Not balanced){self.totals.delta}'
        st1 = '\n/-------|Transaction|---------------------------------\\\n'
        # st1 += f"|  {self.tags}\n"
        # st1 += f"|  {self.sha1}\n"
        st1 += f"|  Νο:{self.id}, ΑΦΜ Συναλλασομένου: {self.afm}\n"
        st1 += f"|  {self.date} {self.par} {self.per} {is_balanced}\n"
        st1 += '\n'.join(['|  ' + i.__str__() for i in self.lines])
        st1 += '\n\\-----------------------------------------------------/\n'
        return st1
