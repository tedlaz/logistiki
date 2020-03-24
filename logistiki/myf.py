from logistiki import parsers as prs
from configparser import ConfigParser
from logistiki.myf2xml import create_xml
from logistiki.logger import logger
import argparse


def main(ini_file='logistiki.ini'):
    logger.info(f'ini_file: {ini_file}')
    cfg = ConfigParser()
    cfg.read(ini_file)
    exclude = cfg['myf']['exclude'].split() or None
    only = cfg['myf']['only'].split() or None
    koybas = cfg['myf']['koybas'].split() or ()
    rfpa = cfg['myf']['reversefpa'].split() or ()
    book = prs.parse_all(dict(cfg['company']), dict(cfg['parse']))
    # book.ee_book_report(exclude=exclude, only=only)
    data = book.myf_xml(
        exclude=exclude, only=only, koybas=koybas, rfpa=rfpa)
    return create_xml(data)


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description='Δημιουργία ΜΥΦ xml')
    pars.add_argument('-o', '--Output', help='Όνομα αρχείου για αποθήκευση')
    pars.add_argument('-i', '--Inifile', help='Όνομα αρχείου ini')
    pars.add_argument('--version', action='version', version='1.0')
    arg = pars.parse_args()
    if arg.Inifile:
        xml_text, afms = main(arg.Inifile)
    else:
        xml_text, afms = main()
    with open('zzz_afms_to_validate.txt', 'w') as fil:
        fil.write('\n'.join(afms))
    print(xml_text)
    if arg.Output:
        with open(arg.Output, 'w') as fil:
            fil.write(xml_text)
            print(f"Το αρχείο {arg.Output} δημιουργήθηκε επιτυχώς !!!")
