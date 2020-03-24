# from logistiki.myf2xml import create_xml
from configparser import ConfigParser
from logistiki import parsers as prs
import argparse


def main(apo, eos, ini_file='logistiki.ini'):
    cfg = ConfigParser()
    cfg.read(ini_file)
    book = prs.parse_all(dict(cfg['company']), dict(cfg['parse']))
    print(book.isozygio(apo=apo, eos=eos))


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description='Ισοζύγιο λογιστικής')
    pars.add_argument('-f', '--From', help='Από ημερομηνία')
    pars.add_argument('-t', '--To', help='Έως ημερομηνία')
    pars.add_argument('--version', action='version', version='1.0')
    arg = pars.parse_args()
    main(arg.From, arg.To)
