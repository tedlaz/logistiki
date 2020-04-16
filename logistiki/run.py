#!/usr/bin/env python
from configparser import ConfigParser
import argparse
import sys


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

    # logistiki
    imp = subp.add_parser('imerologio', help='Ημερολόγιο λογιστικής')
    imp.add_argument('-f', '--from', help='Από ημερομηνία')
    imp.add_argument('-t', '--to', help='Έως ημερομηνία')

    # isozygio
    isop = subp.add_parser('isozygio', help='Ισοζύγιο λογαριασμών')
    isop.add_argument('-f', '--from', help='Από ημερομηνία')
    isop.add_argument('-t', '--to', help='Έως ημερομηνία')

    # kartella
    karp = subp.add_parser('kartella', help='Καρτέλλα λογαριασμού')
    karp.add_argument('account', help='Λογαριασμός')
    karp.add_argument('-f', '--from', help='Από ημερομηνία')
    karp.add_argument('-t', '--to', help='Έως ημερομηνία')

    # myf
    myfp = subp.add_parser(
        'myf',
        help='Συγκεντρωτική Πελατών/Προμηθευτών σε αρχείο xml'
    )
    myfp.add_argument('-o', '--οut', help='Όνομα αρχείου για αποθήκευση')

    # fpa
    fpap = subp.add_parser('fpa', help='ΦΠΑ περιόδου')
    fpap.add_argument('-f', '--from', help='Από ημερομηνία')
    fpap.add_argument('-t', '--to', help='Έως ημερομηνία')
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
        from logistiki import parsers as prs
        cfg = ConfigParser()
        cfg.read(args.inifile)
        book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
        book.ee_book_report(exclude=args.exclude, only=args.only)
        pass
    elif args.command == 'imerologio':
        pass
    elif args.command == 'isozygio':
        pass
    elif args.command == 'kartella':
        pass
    elif args.command == 'myf':
        pass
    elif args.command == 'fpa':
        pass
    elif args.command == 'fpachk':
        pass
    elif args.command == 'xmlchk':
        pass
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
