from decimal import Decimal
from collections import namedtuple, defaultdict
from qlogistiki.utils import gr2dec
from qlogistiki.transaction import Transaction

ValPoint = namedtuple('ValPoint', 'date account delta')
Anoigma = namedtuple('Anoigma', 'date account value')
fpa_prefix = 'ΦΠΑ'


def parse(file):
    """
    Parser for accounting text files
    """
    trn = None
    company_afm = ''
    company_name = ''
    transactions = []
    validations = []
    anoigma = []
    accounts = defaultdict(Decimal)
    tran_total = 0

    with open(file) as fil:
        lines = fil.read().split('\n')

    for line in lines:
        rline = line.rstrip()

        # Αγνόησε τις κενές γραμμές
        if len(rline) == 0:
            continue

        # Αγνόησε τις γραμμές σχολίων
        elif rline.startswith('#'):
            continue

        # Στοιχεία εταιρείας (ΑΦΜ, Πεωνυμία)
        elif rline.startswith('$'):
            _, co_afm, *co_name = rline.split()
            company_afm = co_afm
            company_name = ' '.join(co_name)

        # Εγγραφές ανοίγματος
        elif rline.startswith('<'):
            _, adate, accounta, value = rline.split()
            anoigma.append(Anoigma(adate, accounta, gr2dec(value)))

        # Γραμμή επιβεβαίωσης υπολοίπου
        elif rline.startswith(('@')):
            # @ 2020-05-10 Αγορές.Εμπορευμάτων.εσωτερικού -120,32
            _, cdat, cacc, cval = rline.split()
            validations.append(ValPoint(cdat, cacc, gr2dec(cval)))

        elif rline[:10].replace('-', '').isnumeric():  # Γραμμή Head
            # if status == LINE:
            #     self.add_transaction(trn)
            dat, par, _, per, *afma = rline.split('"')
            dat = dat.strip()
            par = par.strip()
            per = per.strip()
            afm = afma[0].strip() if afma else ''
            trn = Transaction(dat, par, per, afm)
            transactions.append(trn)
            tran_total = 0
        elif rline[:2] == '  ':  # Line detail
            account, *txtval = rline.split()
            val = gr2dec(txtval[0]) if txtval else 0
            # Εδώ δημιουργείται αυτόματα ο λογαριασμός ΦΠΑ
            if account == fpa_prefix:
                account = f'{fpa_prefix}.{trn.last_account.name}'
                pfpa = Decimal(trn.last_account.name.split('.')[-1][3:][:-1])
                calfpa = trn.last_delta * pfpa / Decimal(100)
                trn.fpa_status = 1
                # check fpa here /home/ted/smb/documents/ted-data/tedata
                if abs(val - calfpa) > 0.01:
                    trn.fpa_status = 2
            if val:
                trn.add_line(account, val)
                tran_total += val
            else:
                val = -tran_total
                trn.add_last_line(account)
            accounts[account] += val
        else:  # Υπάρχουν γραμμές που ξεκινούν με μη αποδεκτό χαρακτήρα
            pass
    return company_afm, company_name, transactions, validations, accounts, anoigma
