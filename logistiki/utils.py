from decimal import Decimal, ROUND_HALF_UP
import os
from logistiki.logger import logger
ACCOUNT_SPLITTER = '.'


# From udec.py


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


def startswith_any(txts_tuple: tuple, filters_tuple: tuple) -> bool:
    """
    txt: The text to filter
    txt_tuple: A tuple with values
    Checks if any element of txts_tuple starts with any element of
           filters_tuple
    """
    for txt in txts_tuple:
        for txt_filter in filters_tuple:
            if txt.startswith(txt_filter):
                return True
    return False


def dec2grp(anum):
    return f'{anum}'.replace('.', ',')

# From old ugrdate


def date2gr(adate):
    return f'{adate.day}/{adate.month}/{adate.year}'


def date_gr2iso(greek_date):
    """Μετατρέπει μια Ελληνική ημερομηνία σε iso"""
    dd, mm, yyyy = greek_date.split('/')
    return '%s-%s-%s' % (yyyy, mm, dd)


def date_iso2gr(isodate):
    """Μετατρέπει μια iso ημερομηνία σε Ελληνική"""
    try:
        yyyy, mm, dd = isodate.split('-')
        return f'{dd}/{mm}/{yyyy}'
    except AttributeError:
        return ''


# From account.py

def levels(account: str) -> tuple:
    spl = account.split(ACCOUNT_SPLITTER)
    lvls = [ACCOUNT_SPLITTER.join(spl[: i + 1]) for i in range(len(spl))]
    return tuple([account[0]] + lvls)


def levels_reverse(account: str) -> tuple:
    spl = account.split(ACCOUNT_SPLITTER)
    lvls = [ACCOUNT_SPLITTER.join(spl[: i + 1]) for i in range(len(spl))]
    lvls = [account[0]] + lvls
    lvls.reverse()
    return tuple(lvls)


def read_chart(chart_file):
    """
    Δημιουργεί dictionary με τους ανωτεροβάθμιους λογαριασμούς του
    λογιστικού σχεδίου της μορφής : {'38.00': 'Ταμείο', ...}
    """
    chart = {}
    if os.path.exists(chart_file):
        with open(chart_file) as fil:
            for lin in fil.readlines():
                if len(lin.strip()) < 3:
                    continue
                acc, *name = lin.split()
                chart[acc.strip()] = ' '.join(name)
    else:
        logger.error(f'chart file {chart_file} does not exist. Check your ini')
    return chart
