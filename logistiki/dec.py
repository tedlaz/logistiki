from decimal import Decimal, ROUND_HALF_UP


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


def dec(anum):
    try:
        val = Decimal(anum).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    except:
        val = Decimal(0).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    return val


def dec2gr(anum):
    if anum == 0:
        return ''
    return f'{anum:,.2f}'.replace(',', '|').replace('.', ',').replace('|', '.')


def gr2dec(tnum):
    return dec(tnum.strip().replace('.', '').replace(',', '.'))


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
