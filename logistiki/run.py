#!/usr/bin/env python
from configparser import ConfigParser
import argparse
import sys
from logistiki import parsers as prs
from logistiki.utils import read_chart
from logistiki.myf2xml import create_xml


def myf(cfg, out_file):
    exclude = cfg['myf']['exclude'].split() or None
    only = cfg['myf']['only'].split() or None
    koybas = cfg['myf']['koybas'].split() or ()
    rfpa = cfg['myf']['reversefpa'].split() or ()
    book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
    # book.ee_book_report(exclude=exclude, only=only)
    data = book.myf_xml(
        exclude=exclude, only=only, koybas=koybas, rfpa=rfpa)
    xml_text, afms = create_xml(data)
    print(xml_text)
    if out_file:
        with open('zzz_afms_to_validate.txt', 'w') as fil:
            fil.write('\n'.join(afms))
        with open(out_file, 'w') as fil:
            fil.write(xml_text)
            print(f"Το αρχείο {out_file} δημιουργήθηκε επιτυχώς !!!")


def main():
    parser = argparse.ArgumentParser('logistiki.run')
    parser.add_argument('-i', '--inifile', default='logistiki.ini')
    parser.add_argument('-v', '--version', action='version',
                        version='logistiki.run version:1.0')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info'
    )
    subp = parser.add_subparsers(dest='command')

    # afm
    afmp = subp.add_parser('afm', help='Έλεγχοι ΑΦΜ')
    afmgroup = afmp.add_mutually_exclusive_group(required=True)
    afmgroup.add_argument(
        '-l', '--afms', nargs='+',
        help='Έλεγχοι ΑΦΜ (Αλγοριθμικός και online)',
    )
    afmgroup.add_argument('-f', '--file', help='Αρχείο με ΑΦΜ για έλεγχο')

    # ee
    eep = subp.add_parser('ee', help='Βιβλίο Εσόδων-Εξόδων')
    eep.add_argument('-e', '--exclude', nargs='+',
                     help='Εξαιρούμενοι κωδικοί')
    eep.add_argument('-o', '--only', nargs='+',
                     help='Μόνο αυτοί οι κωδικοί')

    # ee to try:
    eex = subp.add_parser('ee2excell', help='Βιβλίο Εσόδων-Εξόδων σε excell')
    eex.add_argument('-o', '--outfile', help='Αρχείο εξόδου')

    # logistiki
    imp = subp.add_parser('imerologio', help='Ημερολόγιο λογιστικής')
    imp.add_argument('-f', '--from', help='Από ημερομηνία')
    imp.add_argument('-t', '--to', help='Έως ημερομηνία')

    # isozygio
    isop = subp.add_parser('isozygio', help='Ισοζύγιο λογαριασμών')
    isop.add_argument('-f', '--apo', help='Από ημερομηνία')
    isop.add_argument('-t', '--eos', help='Έως ημερομηνία')

    # kartella
    karp = subp.add_parser('kartella', help='Καρτέλλα λογαριασμού')
    karp.add_argument('account', help='Λογαριασμός')
    karp.add_argument('-f', '--apo', help='Από ημερομηνία')
    karp.add_argument('-t', '--eos', help='Έως ημερομηνία')

    # myf
    myfp = subp.add_parser(
        'myf',
        help='Συγκεντρωτική Πελατών/Προμηθευτών σε αρχείο xml'
    )
    myfp.add_argument('-o', '--out', help='Όνομα αρχείου για αποθήκευση')

    # fpa
    fpap = subp.add_parser('fpa', help='ΦΠΑ περιόδου')
    fpap.add_argument('-f', '--apo', help='Από ημερομηνία')
    fpap.add_argument('-t', '--eos', help='Έως ημερομηνία')
    fpap.add_argument('-o', '--out', help='Αρχείο για αποθήκευση')

    # fpachk
    fpachkp = subp.add_parser(
        'fpachk', help='Ελεγχος αναλυτικός εγγραφών με ΦΠΑ')

    # xmlchk
    xmlchkp = subp.add_parser(
        'xmlchk', help='Έλεγχος αρχείου xml συγκεντρωτικής')
    xmlchkp.add_argument('xml_file', help='Αρχείο xml για έλεγχο')

    args = parser.parse_args()

    if args.debug:
        print("debug: " + str(args))

    cfg = ConfigParser()
    cfg.read(args.inifile)

    if args.command == 'afm':
        from logistiki.afm import check_afms
        if args.afms:
            check_afms(args.afms)
        else:
            afm_list = []
            with open(args.file) as fil:
                for lin in fil.readlines():
                    afm_list.append(lin.strip())
            check_afms(afm_list)

    elif args.command == 'ee':
        book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
        book.ee_book_report(exclude=args.exclude, only=args.only)

    elif args.command == 'ee2excell':
        book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
        book.ee_book2excel(filename=args.outfile)

    elif args.command == 'imerologio':
        book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
        for trn in book.transactions:
            book.trans_print(trn['id'])

    elif args.command == 'isozygio':
        book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
        fchart = cfg['accounts']['chart']
        chart = read_chart(fchart)
        print(book.isozygio(apo=args.apo, eos=args.eos, chart=chart))

    elif args.command == 'kartella':
        book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
        print(book.kartella(args.account, apo=args.apo, eos=args.eos))

    elif args.command == 'myf':
        myf(cfg, args.out)

    elif args.command == 'fpa':
        from logistiki.fpa import fpa
        fpa(args.apo, args.eos, args.out)

    elif args.command == 'fpachk':
        from logistiki.fpa_check import check_fpa
        check_fpa(cfg)

    elif args.command == 'xmlchk':
        from logistiki.xml_check import printmyf
        printmyf(args.xml_file)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
