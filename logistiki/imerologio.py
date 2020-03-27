import os
from configparser import ConfigParser
from logistiki import parsers as prs
from logistiki.logger import logger
import argparse


def main(apo, eos, ini_file='logistiki.ini'):
    cfg = ConfigParser()
    cfg.read(ini_file)
    book = prs.parse_all(dict(cfg['company']), dict(cfg['parse']))
    for trn in book.transactions:
        book.trans_print(trn['id'])


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description='Ημερολόγιο λογιστικής')
    pars.add_argument('-f', '--From', help='Από ημερομηνία')
    pars.add_argument('-t', '--To', help='Έως ημερομηνία')
    pars.add_argument('--version', action='version', version='1.0')
    arg = pars.parse_args()
    main(arg.From, arg.To)
