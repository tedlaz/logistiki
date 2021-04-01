import os
from logistiki import parsers as prs
from logistiki.utils import dec
from configparser import ConfigParser


def fpa_errors(tran, acc_fpa, threshold):
    poso = dec(0)
    cfpa = dec(0)
    tfpa = dec(0)
    for lin in tran['lines']:
        acc = lin['account']
        if acc[0] in '1267':
            if acc in acc_fpa:
                cfpa += dec(lin['value'] * acc_fpa[acc] / dec(100))
                poso += lin['value']
        elif acc.startswith('54.00'):
            tfpa += lin['value']
    delta = abs(cfpa - tfpa)
    if delta > threshold:
        return {'tran': tran, 'poso': poso, 'delta': delta,
                'cfpa': cfpa, 'tfpa': tfpa}
    return False


def parse_acc_fpa(cfg):
    fpas = dict(cfg['fpa'])
    fpas = {el: fpas[el].split() for el in fpas}
    acc_fpa = {}
    for cod_fpa, vals in fpas.items():
        cod, fpa = cod_fpa.split('_')
        cod = int(cod)
        fpa = int(fpa)
        for val in vals:
            """Επειδή οι εγγραφές ενδοκοινοτικών δεν έχουν ΦΠΑ και ο
               υπολογισμός γίνεται μόνο για το έντυπο, κατά τον έλεγχο
               βάζουμε την τιμή να είναι 0
            """
            if cod_fpa in ('364_24', ):
                acc_fpa[val] = dec(0)
            else:
                acc_fpa[val] = dec(fpa)
    return acc_fpa


def check_fpa(cfg, threshold=0.01):
    acc_fpa = parse_acc_fpa(cfg)

    book = prs.parse_all(cfg)
    errors = []

    for trn in book.transactions:
        if not trn['is_ee']:
            continue
        err = fpa_errors(trn, acc_fpa, threshold)
        if err:
            errors.append(err)
    if not errors:
        print('Δεν υπάρχουν λάθη στο ΦΠΑ')
    else:
        print(f'Βρέθηκαν τα παρακάτω λάθη στο ΦΠΑ με όριο: {threshold}\n')
        stt = ('{date:<10} {par:<12} {per:<60} {poso:>12} '
               '{cfpa:>12} {tfpa:>12} {delta:>12}\n')
        stf = stt.format(date='Ημερομηνία', par='Παραστατικό',
                         per='Περιγραφή', poso='Ποσό', cfpa='ΦΠΑ σωστό',
                         tfpa='ΦΠΑ Βιβλίων', delta='Διαφορά')
        stf += stt.format(date='----------', par='-----------',
                          per='---------', poso='----', cfpa='---------',
                          tfpa='-----------', delta='-------')
        for err in errors:
            stf += stt.format(date=err['tran']['date'],
                              par=err['tran']['parno'],
                              per=err['tran']['perigrafi'][:59],
                              poso=err['poso'], cfpa=err['cfpa'],
                              tfpa=err['tfpa'], delta=err['delta'])
        print(stf)
