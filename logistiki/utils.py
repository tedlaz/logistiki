"""utils: Varius utilities"""
from decimal import Decimal, ROUND_HALF_UP
# from logging import exception
import os
from logistiki.logger import logger

ACCOUNT_SPLITTER = "."


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
    """Create a Decimal with fixed number of decimal digits"""
    if decimals <= 1:
        decimals = 1
    rounder = Decimal("0." + "0" * (decimals - 1) + "1")
    try:
        val = Decimal(anum).quantize(rounder, rounding=ROUND_HALF_UP)
    except Exception:
        val = Decimal(0).quantize(rounder, rounding=ROUND_HALF_UP)
    return val


def dec2gr(anum):
    """123,456.78 -> 123.456,78"""
    if anum == 0:
        return ""
    return f"{anum:,.2f}".replace(",", "|").replace(".", ",").replace("|", ".")


def gr2dec(tnum):
    """gr2dec"""
    return dec(tnum.strip().replace(".", "").replace(",", "."))


def is_afm(afm):
    """
    Algorithmic validation of Greek Vat Numbers
    """
    if not isNum(afm):
        return False
    if afm.startswith("00000"):
        return False
    if len(afm) != 9:
        return False
    va1 = (
        int(afm[0]) * 256
        + int(afm[1]) * 128
        + int(afm[2]) * 64
        + int(afm[3]) * 32
        + int(afm[4]) * 16
        + int(afm[5]) * 8
        + int(afm[6]) * 4
        + int(afm[7]) * 2
    )
    va2 = va1 % 11
    va3 = va2 % 10
    return va3 == int(afm[8])


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
    """dec2grp"""
    return f"{anum}".replace(".", ",")


# From old ugrdate


def date2gr(adate) -> str:
    """Python date to DD/MM/YYYY"""
    return f"{adate.day}/{adate.month}/{adate.year}"


def date_gr2iso(greek_date):
    """Μετατρέπει μια Ελληνική ημερομηνία σε iso"""
    ddd, mmm, yyyy = greek_date.split("/")
    # return "%s-%s-%s" % (yyyy, mmm, ddd)
    return f"{yyyy}-{mmm}-{ddd}"


# def date_iso2gr(isodate):
#     """Μετατρέπει μια iso ημερομηνία σε Ελληνική"""
#     try:
#         yyyy, mm, dd = isodate.split("-")
#         return f"{dd}/{mm}/{yyyy}"
#     except AttributeError:
#         return ""

def date_iso2gr(iso_date: str) -> str:
    """YYYY-MM-DD -> DD/MM/YYYY"""
    if iso_date == "" or iso_date is None:
        return ""
    yyyy, mmm, ddd = iso_date.split("-")
    return f"{ddd}/{mmm}/{yyyy}"

# From account.py


def levels(account: str) -> tuple:
    """'12.34.56' -> ('1', '12', '12.34', '12.34.56')"""
    spl = account.split(ACCOUNT_SPLITTER)
    lvls = [ACCOUNT_SPLITTER.join(spl[: i + 1]) for i in range(len(spl))]
    return tuple([account[0]] + lvls)


def levels_reverse(account: str) -> tuple:
    """'12.34.56' -> ('12.34.56', '12.34', '12', '1')"""
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
        with open(chart_file, encoding="utf8") as fil:
            for lin in fil.readlines():
                if len(lin.strip()) < 3:
                    continue
                acc, *name = lin.split()
                chart[acc.strip()] = " ".join(name)
    else:
        logger.error(f"chart file {chart_file} does not exist. Check your ini")
    return chart
