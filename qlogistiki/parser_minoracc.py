"""
Parse old minoracc files
"""
from decimal import Decimal
from qlogistiki.utils import fix_account


def parser_minoracc(filename):
    """
    Parse minoraccount file to python dictionary
    """
    trans = []
    accounts = set()
    with open(filename) as fil:
        for line in fil:
            if line.startswith("*"):
                continue
            if len(line) < 14:
                continue
            date, apo, se, poso, per = line.split("|")
            date = date.strip()
            apo = fix_account(apo.strip())
            se = fix_account(se.strip())
            poso = Decimal(poso.strip().replace(",", "."))
            per = per.strip()
            accounts.add(apo)
            accounts.add(se)
            trn = {
                "date": date,
                "par": "",
                "per": per,
                "afm": "",
                "lines": [{"acc": se, "val": poso}, {"acc": apo, "val": -poso}],
            }
            trans.append(trn)
    accounts_list = list(accounts)
    accounts_list.sort()
    return trans, accounts_list
