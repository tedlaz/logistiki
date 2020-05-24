

class Dec:
    __slots__ = ['fval']

    def __init__(self, val=0) -> None:
        if isinstance(val, Dec):
            self.fval = val.fval
            return
        try:
            fval = float(val)
            if fval < 0:
                self.fval = round(fval - 0.001, 2)
            elif fval > 0:
                self.fval = round(fval + 0.001, 2)
            else:
                self.fval = 0
        except Exception:
            self.fval = 0

    def __int__(self):
        return int(self.fval)

    def __float__(self):
        return self.fval

    def __add__(self, other):
        return Dec(self.fval + Dec(other).fval)

    def __radd__(self, other):
        return Dec(self.fval + Dec(other).fval)

    def __sub__(self, other):
        return Dec(self.fval - Dec(other).fval)

    def __rsub__(self, other):
        return Dec(Dec(other).fval - self.fval)

    def __mul__(self, other):
        return Dec(self.fval * Dec(other).fval)

    def __rmul__(self, other):
        return Dec(self.fval * Dec(other).fval)

    def __truediv__(self, other):
        return Dec(self.fval / Dec(other).fval)

    def __rtruediv__(self, other):
        return Dec(Dec(other).fval / self.fval)

    def __neg__(self):
        return Dec(-self.fval)

    def __abs__(self):
        return Dec(abs(self.fval))

    def __eq__(self, other):
        return self.fval == Dec(other).fval

    def __ne__(self, other):
        return self.fval != Dec(other).fval

    def __lt__(self, other):
        return self.fval < Dec(other).fval

    def __le__(self, other):
        return self.fval <= Dec(other).fval

    def __gt__(self, other):
        return self.fval > Dec(other).fval

    def __ge__(self, other):
        return self.fval >= Dec(other).fval

    def __repr__(self):
        return f'Dec({self.fval:.2f})'

    def __str__(self):
        return self.gr

    def __format__(self, format_spec):
        return f"{self.gr0:{format_spec}}"

    @classmethod
    def from_gr(cls, val):
        return cls(val.replace('.', '').replace(',', '.'))

    @property
    def gr0(self):
        """
        0         becomes '0,00'
        123456.78 becomes '123.456,pytest
        123456.70 becomes '123.456,70'
        123456.00 becomes '123.456,00'
        """
        eform = f'{self.fval:,.2f}'
        return eform.replace('.', '|').replace(',', '.').replace('|', ',')

    @property
    def gr(self):
        """
        0         becomes ''
        123456.78 becomes '123.456,78'
        123456.70 becomes '123.456,70'
        123456.00 becomes '123.456,00'
        """
        if self == 0:
            return ''
        eform = f'{self.fval:,.2f}'
        return eform.replace('.', '|').replace(',', '.').replace('|', ',')

    @property
    def grs(self):
        """Greek formated
            0         becomes       '0   '
            123456.00 becomes '123.456   '
            123456.70 becomes '123.456,7 '
            123456.78 becomes '123.456,78'
        """
        if self == 0:
            return '0   '
        ivl, dvl = f'{self.fval:,.2f}'.split('.')
        dlist = list(dvl)
        coma = ','
        if dlist[1] == '0':
            dlist[1] = ' '
            if dlist[0] == '0':
                dlist[0] = ' '
                coma = ' '
        finalint = ivl.replace(',', '.')
        return finalint + coma + dlist[0] + dlist[1]

    @property
    def uid(self):
        return f'{self.fval:.2f}'.replace('.', '')
