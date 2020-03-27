import os
from configparser import ConfigParser
from logistiki import parsers as prs
from logistiki.logger import logger
import argparse


def read_chart(chart_file):
    """
    Δημιουργεί dictionary με τους ανωτεροβάθμιους λογαριασμούς του
    λογιστικού σχεδίου της μορφής : {'38.00': 'Ταμείο', ...}
    """
    chart = {}
    if os.path.exists(chart_file):
        with open(chart_file) as fil:
            for lin in fil.readlines():
                acc, *name = lin.split()
                chart[acc.strip()] = ' '.join(name)
    else:
        logger.error(f'chart file {chart_file} does not exist. Check your ini')
    return chart


def main(apo, eos, ini_file='logistiki.ini'):
    cfg = ConfigParser()
    cfg.read(ini_file)
    book = prs.parse_all(dict(cfg['company']), dict(cfg['parse']))
    fchart = cfg['accounts']['chart']
    chart = read_chart(fchart)
    print(book.isozygio(apo=apo, eos=eos, chart=chart))


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description='Ισοζύγιο λογιστικής')
    pars.add_argument('-f', '--From', help='Από ημερομηνία')
    pars.add_argument('-t', '--To', help='Έως ημερομηνία')
    pars.add_argument('--version', action='version', version='1.0')
    arg = pars.parse_args()
    main(arg.From, arg.To)
