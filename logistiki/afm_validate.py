import argparse
from zeep import Client  # pip install zeep
from logistiki.utils import is_afm

URL = "http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"


def main(afm_list):
    afm_list.sort()
    alg_pass = True
    afm_err = []
    for afm in afm_list:
        if not is_afm(afm):
            afm_err.append(afm)
            alg_pass = False

    if not alg_pass:
        print('Απο αλγοριθμικό έλεγχο προέκυψαν λάθος ΑΦΜ:')
        print(', '.join(afm_err))
        return

    cln = Client(URL)
    responses = []
    for afm in afm_list:
        rsp = cln.service.checkVat('EL', afm)
        if not rsp['valid']:
            afm_err.append(afm)
        else:
            responses.append(rsp)
        print(f"{rsp['vatNumber']} {rsp['valid']} {rsp['name']}")

    with open('validated_afms.txt', 'w') as fil:
        fil.write(
            '\n'.join([f"{i['vatNumber']} {i['name']}" for i in responses]))

    if afm_err:
        afm_err_file = 'zzz_afm_errors.txt'
        with open(afm_err_file, 'w') as fil:
            fil.write('\n'.join(afm_err))
        print(
            'Απο online έλεγχο βρέθηκαν ανενεργά ΑΦΜ και καταχωρήθηκαν '
            f'στο αρχείο: {afm_err_file}'
        )


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description='Επιβεβαίωση ΑΦΜ online')
    pars.add_argument('-l', '--Listafm', nargs='+',
                      help='Λίστα με ΑΦΜ για έλεγχο')
    pars.add_argument('-f', '--File', help='Αρχείο με ΑΦΜ για έλεγχο')
    pars.add_argument('--version', action='version', version='1.0')
    arg = pars.parse_args()
    if arg.Listafm:
        main(arg.Listafm)
    elif arg.File:
        afm_list = []
        with open(arg.File) as fil:
            for lin in fil.readlines():
                afm_list.append(lin.strip())
        main(afm_list)
    else:
        print('error')
    # main(['094421389', '090000045', '099936189', '099951144', '094222211'])
