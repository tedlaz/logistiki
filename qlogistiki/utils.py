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


def dec(anum, decimals=2):
    if decimals <= 1:
        decimals = 1
    rounder = Decimal('0.' + '0' * (decimals - 1) + '1')
    try:
        val = Decimal(anum).quantize(rounder, rounding=ROUND_HALF_UP)
    except:
        val = Decimal(0).quantize(rounder, rounding=ROUND_HALF_UP)
    return val


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


def account_levels(account: str, reversed=False, splitter='.') -> tuple:
    spl = account.split(splitter)
    lvls = [splitter.join(spl[: i + 1]) for i in range(len(spl))]
    if reversed:
        lvls.reverse()
    return tuple(lvls)
