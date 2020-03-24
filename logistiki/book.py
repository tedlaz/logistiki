from logistiki.utils import startswith_any, dec2grp
from logistiki.dec import dec
from logistiki.logger import logger


class Book:
    def __init__(self, co_data, transactions, accounts, afms) -> None:
        self.name = co_data['name']
        self.afm = co_data['afm']
        self.year = co_data['year']
        self.branch = co_data['branch']
        self.accounts = accounts
        self.transactions = transactions
        self.afms = afms

    def isozygio(self, apo=None, eos=None):
        """
        Ισοζύγιο λογαριασμών
        """
        pass

    def fpa_report(self, apo=None, eos=None):
        """
        Αναφορά ΦΠΑ για την περίοδο apo-eos
        """
        pass

    def ee_book(self):
        """
        Βιβλίο εσόδων-εξόδων
        """
        eebook = []
        counter = 0
        for trn in self.transactions:
            if trn['is_ee']:
                counter += 1
                tval = tfpa = 0
                typos = set()
                accounts = set()
                for lin in trn['lines']:
                    if lin['account'][0] in '1267':
                        accounts.add(lin['account'])
                    if lin['account'][0] in '2':
                        tval += lin['value']
                        typos.add('2')
                    elif lin['account'][0] in '6':
                        tval += lin['value']
                        typos.add('6')
                    elif lin['account'][0] == '1':
                        tval += lin['value']
                        typos.add('1')
                    elif lin['account'].startswith('54.00.'):
                        tfpa += lin['value']
                    elif lin['account'][0] == '7':
                        tval += lin['value']
                        typos.add('7')
                eebook.append({
                    'typos': ''.join(sorted(list(typos))),
                    'id': counter,
                    'date': trn['date'],
                    'part': trn['partype'],
                    'parno': trn['parno'],
                    'afm': trn['afm'],
                    'perigrafi': trn['perigrafi'],
                    'value': tval,
                    'fpa': tfpa,
                    'total': tval + tfpa,
                    'accounts': accounts
                })
        return eebook

    def ee_book_report(self, exclude=None, only=None):
        """
        Creates an ee report
        exclude: accounts to exclude from report
        only: only theese accounts to include to report
        """
        tot2 = tot6 = tot7 = 0
        fpa2 = fpa6 = fpa7 = 0
        for trn in self.ee_book():
            if only:
                if not startswith_any(trn['accounts'], only):
                    continue
            if exclude:
                if startswith_any(tuple(trn['accounts']), exclude):
                    continue
            # Εδώ κάνουμε τις αθροίσεις
            if trn['typos'] == '2':
                tot2 += trn['value']
                fpa2 += trn['fpa']
            if trn['typos'] == '6':
                tot6 += trn['value']
                fpa6 += trn['fpa']
            if trn['typos'] == '7':
                tot7 += trn['value']
                fpa7 += trn['fpa']
            trn['eper'] = trn['perigrafi'][:50]
            print(
                '{id:<5}{typos:<3}{date} {afm:<9} {parno:<20} {eper:<50}{value:>12}'
                '{fpa:>12}{total:>12} {accounts}'.format(**trn)
            )
        print('----------------------------------------')
        print(f"Ομάδα 2      : {tot2:>12} {fpa2:>12}")
        print(f"Ομάδα 6      : {tot6:>12} {fpa6:>12}")
        print('----------------------------------------')
        print(f"Σύνολο 2+6   : {tot6+tot2:>12} {fpa6+fpa2:>12}")
        print('\n')
        print(f"Ομάδα 7      : {tot7:>12} {fpa7:>12}")
        print('----------------------------------------')
        print(f"Κέρδος 7-2-6 : {tot7-tot6-tot2:>12} {fpa7-fpa6-fpa2:>12}")
        print('----------------------------------------')

        print(
            f"Parameters(only={only}, exclude={exclude})")

    def myf_xml(self, exclude=None, only=None, koybas=(), rfpa=(), action='replace'):
        """
        Συγκεντρωτικές τιμολογίων πελατών/προμηθευτών σε xml
        """
        data = {
            'action': action,
            'co': {
                'afm': self.afm,
                'month': '12',
                'year': self.year,
                'branch': self.branch
            },
            'gcash': [],
            'oexpenses': {}
        }
        dat = '2019-12-31'
        di1 = {}
        di2 = {}
        di6 = {}
        di7 = {}
        cre = 'credit'
        nor = 'normal'
        tam = {'tamNo': '', 'amount': 0, 'tax': 0, 'date': dat}
        reversed_afm = set()
        for trn in self.ee_book():
            # first we filter records
            if only:
                if not startswith_any(trn['accounts'], only):
                    continue
            if exclude:
                if startswith_any(tuple(trn['accounts']), exclude):
                    continue

            afm = trn['afm']

            if trn['typos'] == '1':
                pass

            elif trn['typos'] in '26':
                # Εάν έχουμε λογαριασμούς χωρίς έκπτωση φπα, επειδή οι
                # εγγραφές είναι συνολικές θα πρέπει πρωτού προχωρήσουμε
                # να αποφορολογήσουμε
                if any(i in rfpa for i in trn['accounts']):
                    if trn['fpa'] == 0:
                        val = dec(trn['value'] / dec(1.24))
                        trn['fpa'] = trn['value'] - val
                        trn['value'] = val
                        reversed_afm.add(afm)

                # Προμηθευτές σε κουβά (πχ ΔΕΗ)
                if afm in koybas:
                    data['oexpenses']['amount'] = data['oexpenses'].get(
                        'amount', 0)
                    data['oexpenses']['amount'] += trn['value']
                    data['oexpenses']['tax'] = data['oexpenses'].get('tax', 0)
                    data['oexpenses']['tax'] += trn['fpa']
                    data['oexpenses']['date'] = data['oexpenses'].get(
                        'date', dat)
                    continue

                # Διαφορετικά κανονικά ανά ΑΦΜ/normal-credit
                di6[afm] = di6.get(afm, {})
                if trn['value'] >= 0:
                    di6[afm][nor] = di6[afm].get(
                        nor,
                        {'afm': afm, 'amount': 0, 'tax': 0,
                         'note': nor, 'invoices': 0,
                         'date': dat, 'nonObl': 0}
                    )
                    di6[afm][nor]['amount'] += trn['value']
                    di6[afm][nor]['tax'] += trn['fpa']
                    di6[afm][nor]['invoices'] += 1
                else:
                    di6[afm][cre] = di6[afm].get(
                        cre,
                        {'afm': afm, 'amount': 0, 'tax': 0,
                         'note': cre, 'invoices': 0,
                         'date': dat, 'nonObl': 0}
                    )
                    di6[afm][cre]['amount'] -= trn['value']
                    di6[afm][cre]['tax'] -= trn['fpa']
                    di6[afm][cre]['invoices'] += 1

            elif trn['typos'] == '7':
                if afm == '':
                    tam['amount'] += trn['value']
                    tam['tax'] += trn['fpa']
                else:
                    di7[afm] = di7.get(afm, {})
                    if trn['value'] >= 0:
                        di7[afm][nor] = di7[afm].get(
                            nor,
                            {'afm': afm, 'amount': 0, 'tax': 0,
                             'note': nor, 'invoices': 0, 'date': dat}
                        )
                        di7[afm][nor]['amount'] += trn['value']
                        di7[afm][nor]['tax'] += trn['fpa']
                        di7[afm][nor]['invoices'] += 1
                    else:
                        di7[afm][cre] = di7[afm].get(
                            cre,
                            {'afm': afm, 'amount': 0, 'tax': 0,
                             'note': cre, 'invoices': 0, 'date': dat}
                        )
                        di7[afm][cre]['amount'] -= trn['value']
                        di7[afm][cre]['tax'] -= trn['fpa']
                        di7[afm][cre]['invoices'] += 1

            else:
                raise ValueError('Αδύνατη περίπτωση !!!')
        logger.info(f"Λογαριασμοί που εξαιρούνται σπό τη ΜΥΦ: {exclude}")
        logger.info(f"ΜΥΦ μόνο για λογαριασμούς: {only}")
        logger.info(f"ΑΦΜ για κουβά εξόδων: {koybas}")
        logger.info(f"Λογαριασμοί για αντιστροφή ΦΠΑ: {rfpa}")
        logger.info(f"ΑΦΜ που έγινε αντιστροφή ΦΠΑ: {reversed_afm}")
        # Έχουμε πλέον τα σύνολα ανα ομάδα
        gexpenses = []
        for afm, decre in sorted(di2.items()):
            for _, val in decre.items():
                val['amount'] = dec2grp(val['amount'])
                val['tax'] = dec2grp(val['tax'])
                gexpenses.append(val)

        # Εγγραφές χωρίς έκπτωση του ΦΠΑ επαναφορά
        for afm, decre in sorted(di6.items()):
            for _, val in decre.items():
                val['amount'] = dec2grp(val['amount'])
                val['tax'] = dec2grp(val['tax'])
                gexpenses.append(val)
        data['gexpenses'] = gexpenses

        grevenues = []
        for afm, decre in sorted(di7.items()):
            for _, val in decre.items():
                val['amount'] = dec2grp(val['amount'])
                val['tax'] = dec2grp(val['tax'])
                grevenues.append(val)
        data['grevenues'] = grevenues
        # Mόνο όταν υπάρχουν τιμές στο gcash
        if tam['amount'] != 0:
            tam['amount'] = dec2grp(tam['amount'])
            tam['tax'] = dec2grp(tam['tax'])
            data['gcash'].append(tam)
        return data

    def kartella(self, code):
        """
        Καρτέλλα λογαριασμού με βάση τον κωδικό
        """
        pass

    def __repr__(self):
        return (
            f"Book(name='{self.name}', "
            f"afm={self.afm}, "
            f"year={self.year}, "
            f"branch='{self.branch}', "
            f"transactions={self.transaction_number}, "
            f"accounts={self.account_number})"
        )

    @property
    def account_number(self):
        """
        Αριθμός λογαριασμών
        """
        return len(self.accounts)

    @property
    def transaction_number(self):
        """
        Αριθμός άρθρων
        """
        return len(self.transactions)
