# from logistiki.myf2xml import create_xml
from configparser import ConfigParser
from logistiki import parsers as prs
import argparse


def main(account, apo, eos, ini_file='logistiki.ini'):
    cfg = ConfigParser()
    cfg.read(ini_file)
    book = prs.parse_all(dict(cfg['company']), cfg['parse']['file_path'])
    print(book.kartella(account, apo=apo, eos=eos))


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description='Καρτέλλα λογαριασμού')
    pars.add_argument('account', help='Λογαριασμός')
    pars.add_argument('-f', '--From', help='Από ημερομηνία')
    pars.add_argument('-t', '--To', help='Έως ημερομηνία')
    pars.add_argument('-i', '--Inifile', help='Όνομα αρχείου ini')
    pars.add_argument('--version', action='version', version='1.0')
    arg = pars.parse_args()
    main(arg.account, arg.From, arg.To)
