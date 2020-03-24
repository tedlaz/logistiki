import datetime as dtm
from collections import namedtuple
# from decimal import Decimal
from typing import List, TypeVar
from logistiki.transaction_line_new import TransactionLine as TLine
from logistiki.transaction_line_new import Numeric
from logistiki.dec import dec, dec2gr

TTran = TypeVar("TTran", bound="Transaction")
Ee = namedtuple('Ee', 'typ note date parastatiko amount fpa total')


class Transaction:
    """Transaction class containing header and Trand lines"""

    def __init__(self, isodate: str, parastatiko: str, perigrafi: str,
                 afm: str = '', _id: int = 0) -> None:
        self.id = _id
        self.date = dtm.date.fromisoformat(isodate)
        self.parastatiko: str = parastatiko
        self.perigrafi: str = perigrafi
        self.afm: str = afm
        self.lines: List[TLine] = []
        self.line_counter: int = 0
        self.debit = self.credit = self.delta = dec(0)

    def __repr__(self):
        txtlin = ','.join(l.__repr__() for l in self.lines)
        return (
            f"Transaction("
            f"date='{self.date.isoformat()}', "
            f"parastatiko='{self.parastatiko}', "
            f"perigrafi='{self.perigrafi}', "
            f"afm='{self.afm}', "
            f"id={self.id}, "
            f"lines=[{txtlin}]"
            ")"
        )

    def __add__(self, other: TTran) -> TTran:
        """
        Δημιουργείται νέα εγγραφή με το άθροισμα των επι μέρους εγγραφών.
        Σημειώσεις:
            1. Η ημερομηνία του νέου άρθρου είναι η ημερομηνία του τρέχοντος
            2. Το ΑΦΜ στο νέο άρθρο είναι του τρέχοντος εκτός και αν αυτό
               είναι κενό οπότε είναι του other.
        """
        # if self.date != other.date:
        #     raise ValueError(f"Dates must be the same")
        date = self.date.isoformat()
        par = f'{self.parastatiko}-{other.parastatiko}'
        per = f'{self.perigrafi}-{other.perigrafi}'
        afm = self.afm if self.afm else other.afm
        new = Transaction(date, par, per, afm)
        for lin in self.lines + other.lines:
            new.add_line(lin.code, lin.decre.dc, lin.decre.value)
        return new

    def __mul__(self, anumber: Numeric) -> TTran:
        fval = dec(anumber)
        new = Transaction(
            self.date.isoformat(), self.parastatiko, self.perigrafi,
            self.afm, self.id
        )
        for lin in self.lines:
            new.add_line(lin.code, lin.decre.dc, lin.decre.value * fval)
        return new

    def __str__(self):
        sok = '' if self.is_complete else f'(Not balanced){self.delta}'
        vls = [
            f"|  {i.code:<20} {i.decre.xreosi:>14} {i.decre.pistosi:>14}"
            for i in self.lines
        ]
        st1 = f'\n/----------< Άρθρο {self.id:<7}>---------------------------\\\n'
        st1 += f"|  ΑΦΜ: {self.afm:<34} Γραμμές: {self.line_counter}\n"
        st1 += f"|  {self.date} {self.parastatiko} {self.perigrafi} {sok}\n"
        st1 += '\n'.join(vls)
        st1 += '\n\\-----------------------------------------------------/\n'
        st1 += f"{'Σύνολα':^23} {self.xreosi:>14} {self.pistosi:>14}"
        return st1

    @property
    def xreosi(self) -> str:
        return dec2gr(self.debit)

    @property
    def pistosi(self) -> str:
        return dec2gr(self.credit)

    @property
    def ypoloipo(self) -> str:
        return dec2gr(self.delta)

    def add_line(self, code: str, debit_credit: int, value) -> None:
        if value == 0:
            raise ValueError(f"Value can't be zero")
        new = TLine(code, debit_credit, value)
        self.lines.append(new)
        self.debit += new.decre.debit
        self.credit += new.decre.credit
        self.delta += new.decre.delta
        self.line_counter += 1

    def add_line_last(self, code: str) -> None:
        if self.line_counter < 1:
            raise ValueError(f"Transaction {self} is empty")
        if self.delta == 0:
            raise ValueError(f"Transaction {self} is already balanced")
        elif self.delta > 0:
            if self.debit == 0:
                self.add_line(code, 1, -self.delta)
            else:
                self.add_line(code, 2, self.delta)
        else:
            if self.credit == 0:
                self.add_line(code, 2, self.delta)
            else:
                self.add_line(code, 1, -self.delta)

    def add_lines_calc(self, code1: str, code2: str, dcr: int, value, percent, code_final='') -> None:
        """
        Δημιουργία δύο τουλάχιστον κινήσεων εκ των οποίων η δεύτερη
        είναι εξαρτημένη από την πρώτη με βάση ένα ποσοστό (percent)
        Εάν έχει τιμή η code_final τότε το άρθρο ολοκληρώνεται με λογαριασμό
        την code_final
        """
        self.add_line(code1, dcr, value)
        self.add_line(code2, dcr, value * percent)
        if code_final:
            self.add_line_last(code_final)

    @property
    def is_complete(self):
        """Εάν η κίνηση είναι ολοκληρωμένη"""
        if self.line_counter > 1 and self.delta == 0:
            return True
        return False

    @property
    def is_ee(self) -> bool:
        """
        Εάν η κίνηση ανήκει στο βιβλίο εσόδων/εξόδων
        """
        for lin in self.lines:
            if lin.code[0] in '1267':
                return True
        return False

    @property
    def is_myf(self) -> bool:
        """
        Εάν η κίνηση συμπεριλαμβάνεται στη ΜΥΦ
        Στην περίπτωση που συμπεριλαμβάνεται έχω τέσσερις υποπεριπτώσεις:
        1. grevenues : Είναι πώληση χονδρικής σε πελάτη με ΑΦΜ
        2. gexpenses : Είναι αγορά χονδρικής από προμηθευτή με ΑΦΜ
        3. gcash     : Είναι πώληση λιανικής
        4. oexpenses : Είναι λοιπά έξοδα συγκεντρωτικά
        """
        return False

    @property
    def is_fpa(self) -> bool:
        """Εάν η κίνηση περιέχει ΦΠΑ"""
        return False

    def ee(self):
        """
        Returns an ee object
        """
        tval = tfpa = dec(0)
        ttyp = note = ''
        isee = False
        for lin in self.lines:
            if lin.code[0] in '126':
                isee = True
                ttyp = 'ejoda'
                if lin.decre.real_dc == 1:
                    note = 'normal'
                else:
                    note = 'credit'
                tval += lin.decre.value_positive
            elif lin.code[0] == '7':
                isee = True
                ttyp = 'esoda'
                if lin.decre.real_dc == 2:
                    note = 'normal'
                else:
                    note = 'credit'
                tval += lin.decre.value_positive
            elif lin.code.startswith('54.00'):
                tfpa += lin.decre.value_positive
        # typ note date parastatiko amount fpa total
        if isee:
            return isee, Ee(ttyp, note, self.date.isoformat(),
                            self.parastatiko, tval, tfpa, tval + tfpa)
        return isee, None


if __name__ == '__main__':
    tr1 = Transaction('2020-01-01', 'TDA--223', 'Malakia', '123123123', 112)
    tr1.add_line('20.00.0013', 2, -100)
    tr1.add_line('54.00.2013', 2, -13)
    # tr1.add_line('50.00.0000', 2, 113)
    tr1.add_line_last('50.00.0000')
    # print(tr1)
    tr2 = Transaction('2020-01-01', 'TDA--224', 'Malakia2', '123123123', 113)
    tr2.add_lines_calc('70.00.013', '54.00.713', 2, 245, .13)
    tr2.add_lines_calc('70.00.024', '54.00.724', 2, 144.56, .24)
    tr2.add_line_last('30.00.023')
    # print(tr2, tr2.is_complete)
    # print(tr1 + tr2)

    tr3 = Transaction('2010-02-15', 'MTF12', 'Δοκιμή')
    tr3.add_line('38.00.0000', 1, 100)
    tr3.add_line('38.01.0001', 2, 100)
    print(tr1)
    print(tr2)
    print(tr1 + tr2)
    print(tr1 * 1.21)
    print(tr1.ee())
    print(tr2.ee())
    print(tr3.ee())
