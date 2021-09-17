#!/usr/bin/env python
"""Module run"""
import os
from configparser import ConfigParser
import argparse
from logistiki import parsers as prs
# from logistiki.utils import read_chart
from logistiki.myf2xml import create_xml
from logistiki.afm import check_afms
from logistiki.fpa import fpa
from logistiki.fpa_check import check_fpa
from logistiki.xml_check import printmyf


def myf(cfg, out_file: str):
    """Δημιουργία αρχείου ΜΥΦ"""
    exclude = cfg["myf"]["exclude"].split() or None
    only = cfg["myf"]["only"].split() or None
    koybas = cfg["myf"]["koybas"].split() or ()
    rfpa = cfg["myf"]["reversefpa"].split() or ()
    book = prs.parse_all(cfg)
    # book.ee_book_report(exclude=exclude, only=only)
    data = book.myf_xml(exclude=exclude, only=only, koybas=koybas, rfpa=rfpa)
    xml_text, afms = create_xml(data)
    print(xml_text)
    if out_file:
        with open("zzz_afms_to_validate.txt", "w", encoding="utf8") as fil:
            fil.write("\n".join(afms))
        with open(out_file, "w", encoding="utf8") as fil:
            fil.write(xml_text)
            print(f"Το αρχείο {out_file} δημιουργήθηκε επιτυχώς !!!")


def command_line_args_parser():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser("logistiki.run")
    parser.add_argument("-i", "--inifile", default="logistiki.ini")
    parser.add_argument(
        "-v", "--version", action="version", version="logistiki.run version:1.4"
    )
    parser.add_argument("--debug", action="store_true",
                        help="Print debug info")
    subp = parser.add_subparsers(dest="command")

    # afm
    afmp = subp.add_parser("afm", help="Έλεγχοι ΑΦΜ")
    afmgroup = afmp.add_mutually_exclusive_group(required=True)
    afmgroup.add_argument(
        "-l",
        "--afms",
        nargs="+",
        help="Έλεγχοι ΑΦΜ (Αλγοριθμικός και online)",
    )
    afmgroup.add_argument("-f", "--file", help="Αρχείο με ΑΦΜ για έλεγχο")

    # ee
    eep = subp.add_parser("ee", help="Βιβλίο Εσόδων-Εξόδων")
    eep.add_argument("-e", "--exclude", nargs="+", help="Εξαιρούμενοι κωδικοί")
    eep.add_argument("-o", "--only", nargs="+", help="Μόνο αυτοί οι κωδικοί")

    # ee to excell:
    eex = subp.add_parser("ee2excell", help="Βιβλίο Εσόδων-Εξόδων σε excell")
    eex.add_argument("outfile", help="Αρχείο εξόδου")

    # logistiki
    imp = subp.add_parser("imerologio", help="Ημερολόγιο λογιστικής")
    imp.add_argument("-f", "--from", help="Από ημερομηνία")
    imp.add_argument("-t", "--to", help="Έως ημερομηνία")

    # isozygio
    isop = subp.add_parser("isozygio", help="Ισοζύγιο λογαριασμών")
    isop.add_argument("-f", "--apo", help="Από ημερομηνία")
    isop.add_argument("-t", "--eos", help="Έως ημερομηνία")

    # kartella
    karp = subp.add_parser("kartella", help="Καρτέλλα λογαριασμού")
    karp.add_argument("account", help="Λογαριασμός")
    karp.add_argument("-f", "--apo", help="Από ημερομηνία")
    karp.add_argument("-t", "--eos", help="Έως ημερομηνία")

    # myf
    myfp = subp.add_parser(
        "myf", help="Συγκεντρωτική Πελατών/Προμηθευτών σε αρχείο xml"
    )
    myfp.add_argument("-o", "--out", help="Όνομα αρχείου για αποθήκευση")

    # fpa
    fpap = subp.add_parser("fpa", help="ΦΠΑ περιόδου")
    fpap.add_argument("-f", "--apo", help="Από ημερομηνία")
    fpap.add_argument("-t", "--eos", help="Έως ημερομηνία")
    fpap.add_argument("-o", "--out", help="Αρχείο για αποθήκευση")
    fpap.add_argument("-y", "--ypo", help="Πιστωτικό υπόλοιπο")

    # fpachk
    # fpachkp = subp.add_parser(
    #     "fpachk", help="Ελεγχος αναλυτικός εγγραφών με ΦΠΑ")
    subp.add_parser("fpachk", help="Ελεγχος αναλυτικός εγγραφών με ΦΠΑ")
    # xmlchk
    xmlchkp = subp.add_parser(
        "xmlchk", help="Έλεγχος αρχείου xml συγκεντρωτικής")
    xmlchkp.add_argument("xml_file", help="Αρχείο xml για έλεγχο")
    return parser


def main():
    """Main program"""
    args_parser = command_line_args_parser()
    args = args_parser.parse_args()

    if args.debug:
        print("debug: " + str(args))

    cfg = ConfigParser()
    if os.path.exists(args.inifile):
        cfg.read(args.inifile, encoding='UTF-8')
    else:
        raise FileNotFoundError("logistiki.ini file does not exist")

    if args.command == "afm":

        if args.afms:
            check_afms(args.afms)
        else:
            afm_list = []
            with open(args.file, encoding="utf8") as fil:
                for lin in fil.readlines():
                    afm_list.append(lin.strip())
            check_afms(afm_list)

    elif args.command == "ee":
        book = prs.parse_all(cfg)
        book.ee_book_report(exclude=args.exclude, only=args.only)

    elif args.command == "ee2excell":
        book = prs.parse_all(cfg)
        book.ee_book2excel(cfg, filename=args.outfile)

    elif args.command == "imerologio":
        book = prs.parse_all(cfg)
        for trn in book.transactions:
            book.trans_print(trn["id"])

    elif args.command == "isozygio":
        book = prs.parse_all(cfg)
        # fchart = cfg["accounts"]["chart"]
        # chart = read_chart(fchart)
        chart = dict(cfg["chart"])
        print(book.isozygio(apo=args.apo, eos=args.eos, chart=chart))

    elif args.command == "kartella":
        book = prs.parse_all(cfg)
        print(book.kartella(args.account, apo=args.apo, eos=args.eos))

    elif args.command == "myf":
        myf(cfg, args.out)

    elif args.command == "fpa":

        # fpa(args.apo, args.eos, args.out)
        fpa(cfg, args)

    elif args.command == "fpachk":

        check_fpa(cfg)

    elif args.command == "xmlchk":

        printmyf(args.xml_file)

    else:
        args_parser.print_help()


if __name__ == "__main__":
    main()
