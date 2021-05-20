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
    rounder = Decimal("0." + "0" * (decimals - 1) + "1")
    correct = Decimal("0." + "0" * (decimals + 1) + "1")
    try:
        valt = Decimal(anum) + correct
        val = valt.quantize(rounder)
    except:
        val = Decimal(0).quantize(rounder)
    return val


def grup(txtval):
    """Trasforms a string to uppercase special for Greek comparison

    :param txtval:
    :return:
    """
    spc = {
        "Ά": "Α",
        "ά": "Α",
        "Έ": "Ε",
        "έ": "Ε",
        "Ή": "Η",
        "ή": "Η",
        "Ί": "Ι",
        "ΐ": "Ι",
        "Ϊ": "Ι",
        "ί": "Ι",
        "ϊ": "Ι",
        "Ό": "Ο",
        "ό": "Ο",
        "Ύ": "Υ",
        "Ώ": "Ω",
        "Ϋ": "Υ",
        "ΰ": "Υ",
        "ϋ": "Υ",
        "ύ": "Υ",
        "ώ": "Ω",
    }
    return "".join(spc.get(i, i) for i in txtval).upper()


def fix_account(account, separator="."):
    """Capitalize and replace separator"""
    acclev = account.split(".")
    return separator.join([i.capitalize() for i in acclev])


def is_afm(a):
    """
    Algorithmic validation of Greek Vat Numbers
    """
    if not isNum(a):
        return False
    if a.startswith("00000"):
        return False
    if len(a) != 9:
        return False
    b = (
        int(a[0]) * 256
        + int(a[1]) * 128
        + int(a[2]) * 64
        + int(a[3]) * 32
        + int(a[4]) * 16
        + int(a[5]) * 8
        + int(a[6]) * 4
        + int(a[7]) * 2
    )
    c = b % 11
    d = c % 10
    return d == int(a[8])


def gr2strdec(greek_number: str) -> str:
    """
    Greek number to text decimal
    """
    return greek_number.replace(".", "").replace(",", ".")


def gr2dec(greek_number: str) -> Decimal:
    """
    Greek number to text decimal
    """
    return dec(gr2strdec(greek_number))


def account_tree(account, reversed=False, splitter=".") -> tuple:
    try:
        spl = account.split(splitter)
    except Exception:
        return ("",)
    lvls = [splitter.join(spl[: i + 1]) for i in range(len(spl))]
    if reversed:
        lvls.reverse()
    return tuple(lvls)


def gr_num(number):
    try:
        ivl, dvl = f"{number:,.2f}".split(".")
        dlist = list(dvl)
    except Exception:
        return "0   "
    coma = ","
    if dlist[1] == "0":
        dlist[1] = " "
        if dlist[0] == "0":
            dlist[0] = " "
            coma = " "
    finalint = ivl.replace(",", ".")
    return finalint + coma + dlist[0] + dlist[1]


def dec2gr(anum):
    if anum == 0:
        return ""
    return f"{anum:,.2f}".replace(",", "|").replace(".", ",").replace("|", ".")
