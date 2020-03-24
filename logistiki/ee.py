# from logistiki.myf2xml import create_xml
from configparser import ConfigParser
from logistiki import parsers as prs
import argparse


def main(exclude, only, ini_file='logistiki.ini'):
    cfg = ConfigParser()
    cfg.read(ini_file)
    book = prs.parse_all(dict(cfg['company']), dict(cfg['parse']))
    book.ee_book_report(exclude=exclude, only=only)


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description='Βιβλίο Εσόδων εξόδων')
    pars.add_argument('-e', '--Exclude', nargs='+',
                      help='Κωδικοί που δεν περιλαμβάνονται')
    pars.add_argument('-o', '--Only', nargs='+',
                      help='Κωδικοί που περιλαμβάνονται')
    pars.add_argument('-i', '--Inifile', help='Όνομα αρχείου ini')
    pars.add_argument('--version', action='version', version='1.0')
    arg = pars.parse_args()
    if arg.Inifile:
        main(arg.Exclude, arg.Only, arg.Inifile)
    else:
        main(arg.Exclude, arg.Only)
