from logistiki.f2_render import f2_render
from logistiki.utils import dec, date_iso2gr
from logistiki import parsers as prs
from configparser import ConfigParser
import argparse


def reverse_fpa_dict(adict: dict) -> dict:
    """Αντιστροφή του dict"""
    reverse = {}
    for cod_fpa, vals in adict.items():
        cod, fpa = cod_fpa.split("_")
        cod = int(cod)
        fpa = int(fpa)
        for val in vals:
            reverse[val] = reverse.get(val, {})
            reverse[val][cod] = fpa
    return reverse


def fpa(cfg, args):  # apo, eos, outfile=None, ini_file='logistiki.ini'):
    """
    Για τον υπολογισμό του φπα χρησιμοποιούμε παραμέτρους από το αρχείο
    logistiki.ini
    """
    # Εδώ δημιουργούμε το {'20.00.24': {363: 24}, ...}
    fpas = dict(cfg["fpa"])
    fpas = {el: fpas[el].split() for el in fpas}

    acc_code_fpa = reverse_fpa_dict(fpas)

    codata = dict(cfg["company"])
    codata["apo"] = date_iso2gr(args.apo)
    codata["eos"] = date_iso2gr(args.eos)
    # Εδώ φορτώνουμε τα δεδομένα στο βιβλίο
    book = prs.parse_all(cfg)
    isozygio = book.totals_for_fpa(args.apo, args.eos)
    fdata = {}
    fpad = {}
    for account, value in isozygio.items():
        if account in acc_code_fpa:
            for code, fpa in acc_code_fpa[account].items():
                fdata[code] = fdata.get(code, dec(0))
                fdata[code] += value
                fpad[code] = fpad.get(code, dec(0))
                fpad[code] += dec(value * dec(fpa) / dec(100))
    fdata[5400] = isozygio[5400]
    for cods in [361, 362, 363, 364, 365, 366]:
        fpa_value = fpad.get(cods, dec(0))
        if fpa_value != 0:  # Για να αποφύγω τις μηδενικές τιμές
            fdata[cods + 20] = fpa_value
    # DATA = {361: dec(95156.97), 303: dec(101119.21), 381: dec(100.34),
    #         306: dec(28529.25), 364: dec(1825.68), 349: dec(39527.90)}
    f2_render(codata, fdata, args.out)
