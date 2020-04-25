import os
import argparse
import readline
from decimal import Decimal
from parser_minoracc import parser_minoracc as parser_ted
OUT, HEAD, LINE = 0, 1, 2


def fix_acc(account, separator='.'):
    """Capitalize and replace separator"""
    acclev = account.split('.')
    return separator.join([i.capitalize() for i in acclev])


def gr_num(number):
    str_number = str(number)
    intp, *decp = str_number.split('.')
    if decp:
        if len(decp[0]) == 1:
            return f"{number:,.1f}".replace(',', '|').replace('.', ',').replace('|', '.') + " "
        else:
            return f"{number:,.2f}".replace(',', '|').replace('.', ',').replace('|', '.')
    return f"{number:,.0f}".replace(',', '.') + '   '


def parse(file):
    """
    Parse new format to python dictionary object
    """
    trans = []
    status = OUT
    lineno = 0
    with open(file) as fil:
        for lin in fil:
            lineno += 1
            if len(lin.strip()) < 10:
                # print(f'Line<12:{lineno}')
                if status == LINE:
                    trans.append(trn)
                status = OUT
                continue

            if lin[0] == '#':  # Γραμμή σχολίου
                #print(f'sxolio: {lineno}')
                continue

            if lin[:10].replace('-', '').isnumeric():  # Γραμμή head
                # Σε περίπτωση που δεν έχουν αφεθεί κενές γραμμές
                #    ανάμεσα σε transactions
                if status == LINE:  # Δεν έχει καταχωρηθεί το προηγούμενο transaction
                    trans.append(trn)
                status = HEAD
                total = 0
                dat, par, _, per, *afma = lin.split('"')
                #dat, sign = dat_sign.split()
                par = par.strip()
                per = per.strip()
                afm = afma[0].strip() if afma else ''
                trn = {'date': dat, 'par': par,
                       'per': per, 'afm': afm, 'lines': []}
            else:
                #print(f'line: {lineno}')
                status = LINE
                account, *value = lin.split()
                if value:
                    value = Decimal(value[0].replace(
                        '.', '').replace(',', '.'))
                    total += Decimal(value)
                else:
                    value = -total
                    total = 0
                trn['lines'].append({'acc': account, 'val': value})
        if status == LINE:
            # print('open')
            trans.append(trn)
    return trans


def writer(data, filename, maxlenacc=30):
    if os.path.exists(filename):
        raise ValueError('file already exists')
    with open(filename, 'w') as fil:
        for trn in data:
            stt = '{date} "{par}" "{per}"\n'
            head = stt.format(
                date=trn['date'], par=trn['par'], per=trn['per'])
            fil.write(head)
            tot = Decimal(0)
            llen = len(trn['lines'])
            for i, lin in enumerate(trn['lines']):
                accn = lin['acc']
                if llen == i + 1:
                    if lin['val'] != -tot:
                        raise ValueError('Το άρθρο δεν είναι ισοσκελισμένο')
                    fil.write(f"  {accn}\n")
                else:
                    value = lin['val']
                    tot += value
                    fil.write(f"  {accn:<{maxlenacc}} {gr_num(value):>12}\n")
            fil.write('\n')


def account_writer(data, filename):
    if os.path.exists(filename):
        raise ValueError('file already exists')
    with open(filename, 'w') as fil:
        fil.write('\n'.join(i for i in data))


def account_reader(acc_file):
    accounts = []
    with open(acc_file) as fil:
        for line in fil:
            accounts.append(line.strip())
    maxlen = max(len(i) for i in accounts)
    return accounts, maxlen


def insert_record(filename, lmoi):
    def completer(text, state):
        options = [x for x in lmoi if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None
    dat = input('Ημερομηνία:').strip()
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    apo = input('Από       : ').strip()
    while apo not in lmoi:
        print('Ο Λογαριασμός αυτός δεν υπάρχει. Προσπαθήστε πάλι')
        apo = input('Από       : ').strip()
    se = input('Σε        : ').strip()
    while se not in lmoi:
        print('Ο Λογαριασμός αυτός δεν υπάρχει. Προσπαθήστε πάλι')
        se = input('Από       : ').strip()
    readline.set_completer(completer)
    val = input('Ποσό      : ').strip()
    val = val.replace(',', '.')
    per = input('Περιγραφή : ').strip()
    tlin = f'\n{dat} "" "{per}"\n'
    tlin += f"  {se:<30} {gr_num(val)}\n"
    tlin += f"  {apo}\n"
    with open(filename, 'a') as afil:
        afil.write(tlin)
    print('Line %s added succesfully...')


def insert_line(lmoi, acc_size):
    def completer(text, state):
        options = [x for x in lmoi if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    acc = input('Λογαριασμός: ').strip()
    if not acc:
        return None, False
    while acc not in lmoi:
        print('Ο Λογαριασμός αυτός δεν υπάρχει. Προσπαθήστε πάλι')
        acc = input('Λογαριασμός : ').strip()
    val = input('Ποσό        : ').strip()
    if val:
        return f"  {acc:<{acc_size}} {gr_num(val):>12}\n", True
    return f"  {acc}\n", False


def insert_full_transaction(filename, lmoi, lmoimax):
    dat = input('Ημερομηνία: ').strip()
    par = input('Παραστατικό: ').strip()
    per = input('Περιγραφή : ').strip()
    afm = input('ΑΦΜ : ').strip()
    tlin = f'\n{dat} "{par}" "{per}" {afm}\n'
    nline, more = insert_line(lmoi, lmoimax)
    tlin += nline
    more = True
    while more:
        new_line, more = insert_line(lmoi, lmoimax)
        if new_line:
            tlin += new_line
    with open(filename, 'a') as afil:
        afil.write(tlin)
    print('Line %s added succesfully...')


def insert_records(filename):
    lmoi, lmoimax = account_reader('accs.txt')
    more = 'Y'
    while more in 'YyΝνNn':
        insert_full_transaction(filename, lmoi, lmoimax)
        more = input('Θέλετε να κάνετε και άλλη εγγραφή ?(Ναί/Οχι): ')


def argument_parse():
    pars = argparse.ArgumentParser(description=u'Λογιστική')
    pars.add_argument('-p', '--Parse', help='Parse and save')
    pars.add_argument('-o', '--Out', help='File name to save')
    pars.add_argument('-d', '--Data', help='Testing Data')
    pars.add_argument('-i', '--Insert', help='Insert new record')
    pars.add_argument('--version', action='version', version='1.0')
    return pars.parse_args()


if __name__ == '__main__':
    args = argument_parse()
    if args.Parse:
        data, accountset = parser_ted(args.Parse)
        if args.Out:
            maxlenacc = max(len(i) for i in accountset) + 1
            writer(data, args.Out)
            accfil = f'{args.Out}.acc'
            account_writer(accountset, accfil)
        else:
            print(data, accountset)
    elif args.Data:
        print(parse(args.Data))
    elif args.Insert:
        insert_records(args.Insert)
