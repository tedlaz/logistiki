from decimal import Decimal, ROUND_HALF_UP, ROUND_UP


def isNum(val):  # is val number or not
    """Check if val is number or not

    :param val: value to check

    :return: True if val is number else False
    """
    try:
        float(val)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


def dec(anum, decimals=2):
    if decimals <= 1:
        decimals = 1
    rounder = Decimal('0.' + '0' * (decimals - 1) + '1')
    correct = Decimal('0.' + '0' * (decimals + 1) + '1')
    try:
        valt = Decimal(anum) + correct
        val = valt.quantize(rounder)
    except:
        val = Decimal(0).quantize(rounder)
    return val


class Dec:
    quantizer = Decimal('0.01')
    correcter = Decimal('0.0001')

    def __init__(self, val):
        try:
            val = Decimal(val) + self.correcter
            self.value = val.quantize(self.quantizer)
        except:
            self.value = Decimal(0)

    @classmethod
    def from_gr(cls, val):
        return cls(val.replace('.', '').replace(',', '.'))

    @property
    def gr0(self):
        """
        0         becomes '0,00'
        123456.78 becomes '123.456,78'
        123456.70 becomes '123.456,70'
        123456.00 becomes '123.456,00'
        """
        eform = f'{self.value:,.2f}'
        return eform.replace('.', '|').replace(',', '.').replace('|', ',')

    @property
    def gr(self):
        """
        0         becomes ''
        123456.78 becomes '123.456,78'
        123456.70 becomes '123.456,70'
        123456.00 becomes '123.456,00'
        """
        if self.value == 0:
            return ''
        eform = f'{self.value:,.2f}'
        return eform.replace('.', '|').replace(',', '.').replace('|', ',')

    @property
    def grs(self):
        """Greek formated
            0         becomes       '0   '
            123456.00 becomes '123.456   '
            123456.70 becomes '123.456,7 '
            123456.78 becomes '123.456,78'
        """
        if self.value == 0:
            return '0   '
        ivl, dvl = f'{self.value:,.2f}'.split('.')
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
    def float(self):
        return float(self.value)

    def __float__(self):
        return self.float

    def __eq__(self, other):
        if isinstance(other, Dec):
            return self.value == other.value
        return self.value == Dec(other).value

    def __ne__(self, other):
        if isinstance(other, Dec):
            return self.value != other.value
        return self.value != Dec(other).value

    def __lt__(self, other):
        if isinstance(other, Dec):
            return self.value < other.value
        return self.value < Dec(other).value

    def __le__(self, other):
        if isinstance(other, Dec):
            return self.value <= other.value
        return self.value <= Dec(other).value

    def __gt__(self, other):
        if isinstance(other, Dec):
            return self.value > other.value
        return self.value > Dec(other).value

    def __ge__(self, other):
        if isinstance(other, Dec):
            return self.value >= other.value
        return self.value >= Dec(other).value

    def __neg__(self):
        return Dec(-self.value)

    def __abs__(self):
        return Dec(abs(self.value))

    def __add__(self, other):
        if isinstance(other, Dec):
            return Dec(self.value + other.value)
        return Dec(self.value + Dec(other).value)

    def __sub__(self, other):
        if isinstance(other, Dec):
            return Dec(self.value - other.value)
        return Dec(self.value - Dec(other).value)

    def __mul__(self, other):
        if isinstance(other, Dec):
            return Dec(self.value * other.value)
        return Dec(self.value * Dec(other).value)

    def __truediv__(self, other):
        if isinstance(other, Dec):
            return Dec(self.value / other.value)
        return Dec(self.value / Dec(other).value)

    def __repr__(self):
        return f'Dec({self.value:,.2f})'

    def __str__(self):
        return f'{self.value:,.2f}'


def fix_account(account, separator='.'):
    """Capitalize and replace separator"""
    acclev = account.split('.')
    return separator.join([i.capitalize() for i in acclev])


def is_afm(a):
    '''
    Algorithmic validation of Greek Vat Numbers
    '''
    if not isNum(a):
        return False
    if a.startswith('00000'):
        return False
    if len(a) != 9:
        return False
    b = int(a[0]) * 256 + int(a[1]) * 128 + int(a[2]) * 64 + int(a[3]) * 32 + \
        int(a[4]) * 16 + int(a[5]) * 8 + int(a[6]) * 4 + int(a[7]) * 2
    c = b % 11
    d = c % 10
    return d == int(a[8])


def gr2strdec(greek_number: str) -> str:
    """
    Greek number to text decimal
    """
    return greek_number.replace('.', '').replace(',', '.')


def gr2dec(greek_number: str) -> Decimal:
    """
    Greek number to text decimal
    """
    return dec(gr2strdec(greek_number))


def account_tree(account: str, reversed=False, splitter='.') -> tuple:
    try:
        spl = account.split(splitter)
    except Exception:
        return ('', )
    lvls = [splitter.join(spl[: i + 1]) for i in range(len(spl))]
    if reversed:
        lvls.reverse()
    return tuple(lvls)


def gr_num(number):
    try:
        ivl, dvl = f'{number:,.2f}'.split('.')
        dlist = list(dvl)
    except Exception:
        return '0   '
    coma = ','
    if dlist[1] == '0':
        dlist[1] = ' '
        if dlist[0] == '0':
            dlist[0] = ' '
            coma = ' '
    finalint = ivl.replace(',', '.')
    return finalint + coma + dlist[0] + dlist[1]


def dec2gr(anum):
    if anum == 0:
        return ''
    return f'{anum:,.2f}'.replace(',', '|').replace('.', ',').replace('|', '.')
