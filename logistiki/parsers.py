import os
from collections import defaultdict
from logistiki.logger import logger
from logistiki.utils import dec, gr2dec, is_afm, date_gr2iso
from logistiki.book import Book


def parse_imerologio(fil: str, encoding="WINDOWS-1253") -> tuple:
    """Parses text file"""
    # Create list with lines to exclude
    EXC = (
        " " * 150 + "Σελίδα",
        " " * 33 + "ΓΕΝΙΚΟ ΗΜΕΡΟΛΟΓΙΟ",
        "  Ημ/νία      Α/Α ΚΒΣ Στοιχεία Αρθρου",
        "  Ημ/νία     Α/Α ΚΒΣ  Στοιχεία Αρθρου",
        "                      Σχετ. Παραστατ.",
        "  -----------------------------------",
        " " * 38 + "Από μεταφορά",
        " " * 123 + "-------------- --------------",
        " " * 70 + "Σύνολα Σελίδας",
        " " * 70 + "Σε Μεταφορά",
        " " * 70 + "Σύνολα Περιόδου",
        " " * 152,
    )
    dat = par = lmo = lmp = xre = pis = pe2 = per = ""
    tno = lno = 0
    SDAT = slice(2, 12)  # Ημερομηνία
    SPAR = slice(22, 48)  # Παραστατικό
    SLMO = slice(48, 60)  # Κωδικός λογαριασμού
    SLMP = slice(77, 122)  # Ονομασία λογαριασμού
    SXRE = slice(124, 137)  # Χρέωση
    SPIS = slice(139, 152)  # Πίστωση
    SPE2 = slice(22, 48)  # Έξτρα περιγραφή
    SPER = slice(48, -1)  # Περιγραφή
    dper = {}
    dlmo = {}
    trah = {}
    trad = {}
    arthra = defaultdict(list)
    unparsed_lines = {}
    with open(fil, encoding=encoding) as ofil:
        for i, lin in enumerate(ofil):
            llin = len(lin)  # Το υπολογίζω εδώ μία φορά
            # print(lin)
            if llin < 48:  # Δεν έχουν νόημα γραμμές μικρότερες του 48
                continue
            elif lin.startswith(EXC):  # Exclude lines
                continue
            elif llin < 132:  # Πρόκειται για γραμμή περιγραφής
                pe2 = lin[SPE2].strip()
                per = lin[SPER].strip()
                dper[tno] = {"perigrafi": per, "lineperigrafi": pe2}
            elif lin[50] == "." and lin[53] == "." and lin[134] == ",":
                if lin[4] == "/" and lin[7] == "/":
                    tno += 1
                    dat = date_gr2iso(lin[SDAT])
                    par = lin[SPAR].strip()
                    trah[tno] = {"date": dat, "parastatiko": par}
                lno += 1
                lmo = lin[SLMO].strip()
                lmp = lin[SLMP].strip()
                xre = gr2dec(lin[SXRE])
                pis = gr2dec(lin[SPIS])
                if lmo in dlmo:
                    if dlmo[lmo] != lmp:
                        if dlmo[lmo] and (not lmp):
                            pass
                        elif (not dlmo[lmo]) and lmp:
                            dlmo[lmo] = lmp
                        else:
                            logger.error(
                                f"Διαφορά στο όνομα {lmo}:  {dlmo[lmo]} -> {lmp}"
                            )
                else:
                    dlmo[lmo] = lmp
                trad[lno] = {"id": tno, "code": lmo, "debit": xre, "credit": pis}
                arthra[tno].append(lno)
            else:
                unparsed_lines[i] = lin
    if len(unparsed_lines) > 0:
        logger.error(f"parse_imerologio unparsed lines : {unparsed_lines}")
    else:
        logger.info(f"Transactions and accounts parsed fine from {fil} !!!")
    transactions = []
    for trid, header in trah.items():
        par_type, par_no = header["parastatiko"].split("--")
        tran = {
            "id": trid,
            "date": header["date"],
            "partype": par_type,
            "parno": par_no,
            "perigrafi": dper[trid]["perigrafi"],
            "perigr2": dper[trid]["lineperigrafi"],
            "lines": [],
        }
        tdebit = tcredit = 0
        is_ee = False
        for idd in arthra[trid]:
            tdebit += trad[idd]["debit"]
            tcredit += trad[idd]["credit"]
            typ = val = 0
            if trad[idd]["debit"] == 0:
                typ = 2
                val = trad[idd]["credit"]
            elif trad[idd]["credit"] == 0:
                typ = 1
                val = trad[idd]["debit"]
            if typ == 0:
                raise ValueError(f"{trad[idd]} debit or credit")
            tran["lines"].append(
                {"account": trad[idd]["code"], "typ": typ, "value": val}
            )
            if trad[idd]["code"][0] in "1267":
                is_ee = True
        if tdebit != tcredit:
            raise ValueError(f"Transaction {tran} is not balanced")
        tran["total"] = tdebit
        tran["is_ee"] = is_ee
        transactions.append(tran)
    logger.debug("About to return parsed transactions and accounts!!!")
    return transactions, dlmo


# Kin = namedtuple('Kin', "id dat typ ee par per afm csy val fpa tot")
ESEJ = {
    "ΠΑΓ": 2,
    "ΤΠΥ": 1,
    "ΤΠΛ": 1,
    "ΑΠΥ": 1,
    "ΑΠΛ": 1,
    "ΤΑΓ": 2,
    "ΠΙΣ": 1,
    "ΕΠΛ": 1,
    "ΤΠΕ": 1,
}


def parse_esex(fil, enc="WINDOWS-1253"):
    # Create list with lines to exclude
    logger.debug(f"Starting to parse {fil} file")
    EXC = (
        " " * 164 + "Σελίδα",
        "   Κινήσεις ανά Ημέρα",
        "     A/A Τύπος Εγγραφής",
        "-------- ------------------------- ",
        "   Σύνολα ημέρας",
        " " * 92 + "-------------------- -------------------- ",
        " " * 53 + "Σύνολα Εξόδων",
        " " * 53 + "Σύνολα Εξόδων",
        "  Γενικά Σύνολα",
        " " * 53 + "Εξόδων",
    )
    SDAT = slice(32, 42)  # Ημερομηνία
    SAA = slice(0, 8)  # Αριθμός άρθρου
    STYP = slice(9, 34)  # Τύπος
    SPAR = slice(35, 66)  # Παραστατικό
    SAFM = slice(67, 76)  # ΑΦΜ
    SLMO = slice(67, 91)  # όλο το πεδίο άν δεν υπάρχει ΑΦΜ
    SLMP = slice(77, 91)  # μόνο μετά το ΑΦΜ
    SVAL = slice(93, 112)  # Καθαρή αξία
    SFPA = slice(114, 133)  # ΦΠΑ
    STOT = slice(156, 175)  # Σύνολο
    dat = typ = par = per = afm = ""
    aar = val = fpa = tot = 0
    lines = []
    lines3 = defaultdict(lambda: defaultdict(lambda: {"afm": ""}))
    types = set()
    with open(fil, encoding=enc) as ofil:
        for lin in ofil:
            llin = len(lin)
            if llin < 40:
                continue
            elif lin.startswith(EXC):  # Exclude lines
                continue
            elif lin.startswith("  Κινήσεις της "):
                # print(lin)
                dat = date_gr2iso(lin[SDAT])
            elif lin[109] == "," and lin[130] == "," and lin[151]:
                aar = int(lin[SAA].strip())
                typ = lin[STYP].strip()
                ee = ESEJ[typ]
                par = lin[SPAR].strip()
                # afm = lin[SAFM].strip()
                # if is_afm(afm):
                #     per = lin[SLMP].strip()
                csy = ""

                afm, *per = lin[SLMO].strip().split()
                per = " ".join(per)
                # afm = '000000000'
                val = gr2dec(lin[SVAL])
                fpa = gr2dec(lin[SFPA])
                tot = gr2dec(lin[STOT])
                partyp, parno = par.split()
                lines.append(
                    {
                        "id": aar,
                        "date": dat,
                        "type": typ,
                        "ee": ee,
                        "partyp": partyp,
                        "parno": parno,
                        "perigrafi": per,
                        "afm": afm,
                        "syn_code": csy,
                        "value": val,
                        "fpa": fpa,
                        "total": tot,
                    }
                )
                lines3[dat][parno] = {"afm": afm, "value": val, "fpa": fpa}
                types.add(typ)
    logger.info(f"ee lines and types parsed without errors from {fil} !!!")
    return lines3, types


def parse_afm(fil, enc="WINDOWS-1253"):
    EXCLUDE = (
        " " * 109 + "Σελίδα",
        " " * 44 + "Κατηγορία ",
        "  Oνομα / Επωνυμία ",
        "  ----------------------------------------- ",
    )
    SEPON = slice(2, 44)
    COD53 = slice(54, 66)
    SCOD2 = slice(56, 68)
    SAFM = slice(87, 96)
    # Create list with lines to exclude
    epo = cod = afm = ""
    by_code = defaultdict(lambda: {"eponymia": "", "afm": "", "syn_code": ""})
    ignore_next_line = False
    with open(fil, encoding=enc) as ofil:
        for lin in ofil:
            llin = len(lin)
            if llin < 60:  # 86:
                continue
            if lin.startswith(EXCLUDE):  # Exclude lines
                continue

            if llin > 86:
                epo = lin[SEPON].strip()
                cod = lin[COD53].strip()
                afm = lin[SAFM].strip()
                if cod.startswith("53."):
                    # if afm:
                    by_code[cod] = {"eponymia": epo, "afm": afm, "syn_code": cod}
                    ignore_next_line = True
                else:
                    ignore_next_line = False
            else:
                if ignore_next_line:
                    continue
                else:
                    cod = lin[SCOD2].strip()
                    # if afm:
                    by_code[cod] = {"eponymia": epo, "afm": afm, "syn_code": cod}
    logger.info(f"AFM data parsed without errors from {fil} !!!")
    return by_code


def files_from_path(filepath):
    file_afm = os.path.join(filepath, "afm.txt")
    file_el = os.path.join(filepath, "el.txt")
    file_ee = os.path.join(filepath, "ee.txt")
    return (file_afm, file_ee, file_el)


def parse_varius(ee_file, enc="WINDOWS-1253"):
    fil = open(ee_file, encoding=enc)
    title = next(fil).split("-")[0].strip()
    next(fil)
    lindat = next(fil)
    apo, eos, etos = lindat[85:95], lindat[113:123], lindat[91:95]
    print(title, apo, eos, etos)
    fil.close()


def parse_all(config_parser) -> Book:
    """
    Τρέχουν όλοι οι parsers και παίρνουμε σαν έξοδο ένα βιβλίο λογιστικής
    """
    co_data = dict(config_parser["company"])
    file_path = config_parser["parse"]["file_path"]
    file_afm, file_ee, file_el = files_from_path(file_path)
    # print(file_afm, file_ee, file_el)
    afms = parse_afm(file_afm)
    eelines, eetypes = parse_esex(file_ee)
    transactions, accounts = parse_imerologio(file_el)
    for trn in transactions:
        trn["afm"] = eelines[trn["date"]][trn["parno"]]["afm"]
        if trn["afm"] == "":
            for lin in trn["lines"]:
                if lin["account"].startswith("53."):
                    trn["afm"] = afms[lin["account"]]["afm"]
                    break
        else:
            if not is_afm(trn["afm"]):
                trn["afm"] = afms[trn["afm"]]["afm"]
    return Book(co_data, transactions, accounts, afms)
