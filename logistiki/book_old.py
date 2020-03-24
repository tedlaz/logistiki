"""Book of transactions Module"""
import datetime as dtm
from decimal import Decimal
from collections import namedtuple
import operator
from logistiki.dec import dec, dec2gr
from logistiki.grdate import date2gr
from logistiki.transaction import Transaction
from logistiki.account import AccountContainer, levels_reverse
from logistiki.logger import logger

TDelta = namedtuple('TDelta', 'account_code value')


class IsozygioLine:
    """Test class"""

    def __init__(self,
                 _id='',
                 date='',
                 acc='',
                 par='',
                 per='',
                 debit=0,
                 credit=0):
        self.id = _id
        self.date = date
        self.acc = acc
        self.par = par
        self.per = per
        self.debit = dec(debit)
        self.credit = dec(credit)

    @property
    def delta(self):
        return self.debit - self.credit


class Book:
    """Class Book"""

    def __init__(self, name):
        self.name = name
        self.accounts = AccountContainer()
        self.trans = []

    def add_transaction_object(self, transaction):
        """Add a Transaction object"""
        if not isinstance(transaction, Transaction):
            raise ValueError(f"parameter transaction is not Transaction")
        self.trans.append(transaction)
        for lin in transaction.lines:
            self.accounts.add_account(lin.account.code, lin.account.name)

    def add_transaction_from_dic(self, transaction_dict):
        """Create a new Transaction from a dictionary and add it"""
        self.trans.append(Transaction.tran_from_dic(transaction_dict))
        for lin in transaction_dict['lines']:
            self.accounts.add_account(lin['account'], '')

    def add_transactions_from_ntuples(self, named_tuples):
        """Create a new trasaction from named tuple and add it"""
        for ntuple in named_tuples:
            self.trans.append(Transaction.tran_from_ntuple(ntuple))

    def add_transactions_from_list(self, tran_list):
        """Add Transactions from a list of dictionaries"""
        for elm in tran_list:
            self.add_transaction_from_dic(elm)

    def isozygio(self, apo=None, eos=None, level=1):
        """Calculate Isozygio of a certain degree"""
        dapo = dtm.date.fromisoformat(apo) if apo else dtm.date(1900, 1, 1)
        deos = dtm.date.fromisoformat(eos) if eos else dtm.date(3000, 1, 1)
        assert dapo <= deos
        iso = {}
        txr = tpi = typ = 0
        for tra in self.trans:
            if dapo <= tra.date <= deos:
                for lin in tra.lines:
                    gcode = lin.account.level(level)
                    iso[gcode] = iso.get(
                        gcode, {'debit': dec(0), 'credit': dec(0)})
                    iso[gcode]['debit'] += lin.debit
                    iso[gcode]['credit'] += lin.credit
                    txr += lin.debit
                    tpi += lin.credit
                    typ += lin.debit - lin.credit
        if apo:
            tapo = f' Από: {date2gr(dapo)}'
        else:
            tapo = ''
        if eos:
            teos = f' Έως: {date2gr(deos)}'
        else:
            teos = ''
        tapoeos = f'{tapo}{teos}'
        tmp = f"\n{'ΙΣΟΖΥΓΙΟ ΛΟΓΙΣΤΙΚΗΣ':^104}\n"
        tmp += f"{tapoeos:^104}\n"
        tmp += '-' * 104 + '\n'
        for acc in sorted(iso):
            delta = dec2gr(iso[acc]['debit'] - iso[acc]['credit'])
            accp = self.accounts.closest_name(acc)
            tmp += (
                f"{acc:<15}{accp:<50} {dec2gr(iso[acc]['debit']):>12} "
                f"{dec2gr(iso[acc]['credit']):>12} {delta:>12}\n"
            )
        tmp += '-' * 104 + '\n'
        tmp += (
            f"{'':<15}{'Σύνολα':^50} {dec2gr(txr):>12} "
            f"{dec2gr(tpi):>12} {dec2gr(typ):>12}\n"
        )
        return tmp

    def isozygio_full(self, apo=None, eos=None):
        """Create full isozygio"""
        dapo = dtm.date.fromisoformat(apo) if apo else dtm.date(1900, 1, 1)
        deos = dtm.date.fromisoformat(eos) if eos else dtm.date(3000, 1, 1)
        assert dapo <= deos
        iso = {}
        txr = tpi = typ = 0
        for tra in self.trans:
            if dapo <= tra.date <= deos:
                for lin in tra.lines:
                    gcode = lin.account.code
                    iso[gcode] = iso.get(
                        gcode, {'debit': dec(0), 'credit': dec(0)})
                    iso[gcode]['debit'] += lin.debit
                    iso[gcode]['credit'] += lin.credit
                    txr += lin.debit
                    tpi += lin.credit
                    typ += lin.debit - lin.credit
        fiso = {}
        apot = 0
        for code, val in iso.items():
            for lcode in levels_reverse(code):
                fiso[lcode] = fiso.get(
                    lcode, {'debit': dec(0), 'credit': dec(0)})
                fiso[lcode]['debit'] += val['debit']
                fiso[lcode]['credit'] += val['credit']
            if code[0] in '267':
                apot += val['debit'] - val['credit']
        if apo:
            tapo = f' Από: {date2gr(dapo)}'
        else:
            tapo = ''
        if eos:
            teos = f' Έως: {date2gr(deos)}'
        else:
            teos = ''
        tapoeos = f'{tapo}{teos}'
        tmp = f"\n{'ΙΣΟΖΥΓΙΟ ΛΟΓΙΣΤΙΚΗΣ':^104}\n"
        tmp += f"{tapoeos:^104}\n"
        tmp += '-' * 104 + '\n'
        for acc in sorted(fiso):
            delta = dec2gr(fiso[acc]['debit'] - fiso[acc]['credit'])
            accp = self.accounts.closest_name(acc)
            tmp += (
                f"{acc:<15}{accp:<50} {dec2gr(fiso[acc]['debit']):>12} "
                f"{dec2gr(fiso[acc]['credit']):>12} {delta:>12}\n"
            )
        tmp += '-' * 104 + '\n'
        tmp += (
            f"{'':<15}{'Σύνολα':^50} {dec2gr(txr):>12} "
            f"{dec2gr(tpi):>12} {dec2gr(typ):>12}\n"
            f"{'':<15}{'Αποτέλεσμα (2, 6, 7)':^50} {dec2gr(0):>12} "
            f"{dec2gr(0):>12} {dec2gr(apot):>12}\n"
        )
        return tmp

    def fpa_report(self, apo, eos):
        """
        Create a FPA report
        """
        pass

    def check_fpa(self):
        """
        Εδώ κάνουμε έλεγχο ΦΠΑ σε επίπεδο άρθρου
        """
        lmo_fpa, lmo_pos = self.account_mach()
        diffs = []
        for tran in self.trans:
            apot_lines, fpa_lines = tran.get_fpa_apot()
            if not apot_lines:  # Δεν έχει αποτελεσματικό λ/μο (1, 2, 6, 7)
                continue
            for acc, lin in apot_lines.items():
                if acc in lmo_pos:
                    try:
                        cfpa = dec(lin.value * dec(lmo_pos[acc] / 100))
                        delta = dec(fpa_lines[lmo_fpa[acc]].value - cfpa)
                        if abs(delta) > 0.02:
                            diffs.append((tran, delta))
                    except KeyError:
                        logger.critical(f'{tran}, {lmo_fpa[acc]}')
        if diffs:
            print('There are errors in fpa:')
            for el in diffs:
                print(el[0], el[1])
            return False
        else:
            print('fpa is ok')
            return True

    def apotelesmata(self, apo=None, eos=None):
        """
        Αποτελέσματα
        """
        totals = {}
        for tran in self.trans:
            isee, ee = tran.ee()
            if isee:
                key = f'{ee.typ}-{ee.xrpi}-{ee.ptyp}'
                totals[key] = totals.get(key, 0)
                totals[key] += ee.val
                # typ xrpi date par val fpa tot
                print(
                    f"{ee.typ} {ee.xrpi} {ee.date} {ee.ptyp} {ee.par:<30} "
                    f" {ee.val:>12.2f}{ee.fpa:>12.2f} {ee.tot:>12.2f}"
                )
        # for dat, tot in chksg.items():
        #     print(dat, tot)
        print(totals)

    def sygkentrotiki(self, apo=None, eos=None):
        """
        Δημιουργία συγκεντρωτικής τιμολογίων
        """
        totals = {}
        for tran in self.trans:
            isapo, myf = tran.myf()
            if isapo:
                typ, num = myf.par.split('--')
                key = f'{myf.typ}-{myf.xrpi}'
                totals[key] = totals.get(key, 0)
                totals[key] += myf.val
                # typ xrpi date par val fpa tot
                print(
                    f"{myf.typ} {myf.xrpi} {myf.date} {typ} {num:<30} "
                    f" {myf.val:>12.2f}{myf.fpa:>12.2f} {myf.tot:>12.2f}"
                )
        # for dat, tot in chksg.items():
        #     print(dat, tot)
        print(totals)

    def ee_book(self):
        """
        returns esoda ejoda book
        """
        pass

    def kartella(self, account_code, apo=None, eos=None):
        """
        Μας δίνει την καρτέλλα του λογαριασμού
        id ημερομηνία παραστατικό περιγραφή χρεωση πίστωση υπόλοιπο
        -------------------------------------------------------------
                      από μεταφορά            100.34  30.88     20.33
        12  10/1/2020   ΤΔΑ322      αγορες     10.35
        """
        dapo = dtm.date.fromisoformat(apo) if apo else dtm.date(1900, 1, 1)
        deos = dtm.date.fromisoformat(eos) if eos else dtm.date(3000, 1, 1)
        assert dapo <= deos
        tdelta = dec(0)
        prin = {'id': '', 'dat': '', 'acc': '', 'par': 'Aπό μεταφορά',
                'per': '', 'debit': dec(0), 'credit': dec(0), 'delta': dec(0)}
        per = []
        meta = {'id': '', 'dat': '', 'acc': '', 'par': 'Επόμενες εγγραφές', 'per': '',
                'debit': dec(0), 'credit': dec(0), 'delta': dec(0)}
        for trn in sorted(self.trans):
            for lin in trn.lines:
                if lin.account.code.startswith(account_code):
                    if trn.date < dapo:
                        prin['debit'] += lin.debit
                        prin['credit'] += lin.credit
                        tdelta += lin.debit - lin.credit
                        prin['delta'] = tdelta
                    elif dapo <= trn.date <= deos:
                        tdelta += lin.debit - lin.credit
                        adi = {
                            'id': trn.id,
                            'dat': date2gr(trn.date),
                            'acc': lin.account.code,
                            'par': trn.par[:20],
                            'per': trn.per[:45],
                            'debit': dec2gr(lin.debit),
                            'credit': dec2gr(lin.credit),
                            'delta': dec2gr(tdelta)
                        }
                        per.append(adi)
                    else:
                        meta['debit'] += lin.debit
                        meta['credit'] += lin.credit
                        tdelta += lin.debit - lin.credit
                        meta['delta'] = tdelta
        if prin['delta'] == 0:
            dprin = []
        else:
            prin['debit'] = dec2gr(prin['debit'])
            prin['credit'] = dec2gr(prin['credit'])
            prin['delta'] = dec2gr(prin['delta'])
            dprin = [prin]
        if meta['delta'] == 0:
            dmeta = []
        else:
            meta['debit'] = dec2gr(meta['debit'])
            meta['credit'] = dec2gr(meta['credit'])
            meta['delta'] = dec2gr(meta['delta'])
            dmeta = [meta]
        data = dprin + per + dmeta
        tit = {
            'id': 'AA', 'dat': 'Ημ/νία', 'acc': 'Λογαριασμός',
            'par': 'Παραστατικό', 'per': 'Περιγραφή',
            'debit': 'Χρέωση', 'credit': 'Πίστωση', 'delta': 'Υπόλοιπο'
        }
        fst = (
            "{id:<4} {dat:10} {acc:<15} {par:<20} {per:<45} "
            "{debit:>12} {credit:>12} {delta:>12}\n"
        )
        st1 = f"\nΚαρτέλλα λογαριασμού {account_code}\n"
        if apo:
            st1 += f'Aπό: {date2gr(dapo)}\n'
        if eos:
            st1 += f'Έως: {date2gr(deos)}\n'
        st1 += fst.format(**tit)
        st1 += '-' * 137 + '\n'
        for line in data:
            st1 += fst.format(**line)
        return st1

    def delta(self, account) -> TDelta:
        """
        Επιστρέφει το υπόλοιπο του λογαριασμού
        """
        ndelta = dec(0)
        for tran in self.trans:
            for lin in tran.lines:
                if lin.account.code.startswith(account):
                    ndelta += lin.flat_value
        return TDelta(account, ndelta)

    def unique_fingerprints(self) -> list:
        """Δημιουργία μοναδικού αναγνωριστικού"""
        uf1 = set()
        for tran in self.trans:
            uf1.add(tran.fingerprint)
        return sorted(list(uf1))

    def print_trans_by_fingerprint(self, fingerprint):
        """"""
        for tran in self.trans:
            if fingerprint == tran.fingerprint:
                print(tran)

    def account_mach(self) -> tuple:
        """

        """
        prs = []
        pr2 = {}
        lmo_fpa = {}
        lmo_pososto = {}
        for tran in self.trans:
            for pair in tran.account_pairs():
                if pair:
                    pr2[pair[0]] = pr2.get(pair[0], {})
                    pr2[pair[0]][pair[1]] = pr2[pair[0]].get(pair[1], 0)
                    pr2[pair[0]][pair[1]] += 1
        for key in sorted(pr2):
            if len(pr2[key]) == 1:
                fpa = list(pr2[key].keys())[0]
                prs.append((key, fpa, int(fpa[-2:])))
                lmo_fpa[key] = fpa
                lmo_pososto[key] = int(fpa[-2:])
            else:
                fpa = max(pr2[key].items(), key=operator.itemgetter(1))[0]
                prs.append((key, fpa, int(fpa[-2:])))
                lmo_fpa[key] = fpa
                lmo_pososto[key] = int(fpa[-2:])
        return lmo_fpa, lmo_pososto
