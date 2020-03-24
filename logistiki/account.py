from enum import Enum
ACCOUNT_SPLITTER = '.'
BIBLIO_EE = '1267'
APOTELESMATA = '267'
FPA = '54.00'
TYPOI = (
    'ΤΑΞΕΩΣ ΠΑΓΙΑ ΑΠΟΘΕΜΑΤΑ ΑΠΑΙΤΗΣΕΙΣ ΚΕΦΑΛΑΙΟ ΥΠΟΧΡΕΩΣΕΙΣ ΕΞΟΔΑ ΕΣΟΔΑ '
    'ΑΠΟΤΕΛΕΣΜΑΤΑ ΤΑΞΕΩΣ'
).split()


def levels(account: str) -> tuple:
    spl = account.split(ACCOUNT_SPLITTER)
    lvls = [ACCOUNT_SPLITTER.join(spl[: i + 1]) for i in range(len(spl))]
    return tuple([account[0]] + lvls)


def levels_reverse(account: str) -> tuple:
    spl = account.split(ACCOUNT_SPLITTER)
    lvls = [ACCOUNT_SPLITTER.join(spl[: i + 1]) for i in range(len(spl))]
    lvls = [account[0]] + lvls
    lvls.reverse()
    return tuple(lvls)


class AccountTyp(Enum):
    pagia = 1
    agores = 2
    ejoda = 6
    esoda = 7
    agorejoda = 26
    loipa = 345
    fpa = 5400


class Account:
    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name

    def level(self, level: int = 0) -> str:
        levels = self.levels
        if level < len(levels):
            return levels[level]
        return self.code

    @property
    def typos(self) -> AccountTyp:
        if self.code.startswith(FPA):
            return AccountTyp.fpa
        elif self.code[0] in '26':
            return AccountTyp.agorejoda
        elif self.code[0] == '7':
            return AccountTyp.esoda
        else:
            return AccountTyp.loipa

    @property
    def omada_name(self):
        return TYPOI[int(self.omada)]

    @property
    def omada_default_typ(self) -> int:
        if self.omada in [0, 1, 2, 3, 6, 9]:
            return 1
        return 2

    @property
    def omada(self) -> int:
        return int(self.code[0])

    @property
    def levels(self) -> tuple:
        spl = self.code.split(ACCOUNT_SPLITTER)
        lvls = [ACCOUNT_SPLITTER.join(spl[: i + 1]) for i in range(len(spl))]
        lvls = [self.code[0]] + lvls
        return tuple(lvls)

    @property
    def is_ee(self) -> bool:
        if self.code[0] in BIBLIO_EE:
            return True
        return False

    @property
    def is_apotelesma(self) -> bool:
        if self.code[0] in APOTELESMATA:
            return True
        return False

    @property
    def is_fpa(self) -> bool:
        if self.code.startswith(FPA):
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self.code == other.code

    def __repr__(self):
        return f"Account(code='{self.code}', name='{self.name}')"

    def __str__(self):
        name = self.name or 'NO-NAME'
        return f"{self.code}: {name}"


class AccountContainer:
    def __init__(self):
        self.accounts = {}
        self.add_defult_accounts()

    def add_defult_accounts(self):
        self.add_account('1', 'ΠΑΓΙΑ')
        self.add_account('2', 'ΑΠΟΘΕΜΑΤΑ')
        self.add_account('3', 'ΑΠΑΙΤΗΣΕΙΣ')
        self.add_account('4', 'ΚΕΦΑΛΑΙΟ')
        self.add_account('5', 'ΥΠΟΧΡΕΩΣΕΙΣ')
        self.add_account('6', 'ΕΞΟΔΑ')
        self.add_account('7', 'ΕΣΟΔΑ')
        self.add_account('8', 'ΑΠΟΤΕΛΕΣΜΑΤΑ')
        self.add_account('20', 'ΕΜΠΟΡΕΥΜΑΤΑ')
        self.add_account('24', 'Α & Β ΥΛΕΣ')
        self.add_account('25', 'ΑΝΑΛΩΣΙΜΑ')
        self.add_account('30', 'ΠΕΛΑΤΕΣ')
        self.add_account('33', 'ΧΡΕΩΣΤΕΣ ΔΙΑΦΟΡΟΙ')
        self.add_account('38', 'ΧΡΗΜΑΤΙΚΑ ΔΙΑΘΕΣΙΜΑ')
        self.add_account('38.00', 'ΤΑΜΕΙΟ')
        self.add_account('38.03', 'ΚΑΤΑΘΕΣΕΙΣ')
        self.add_account('50', 'ΠΡΟΜΗΘΕΥΤΕΣ')
        self.add_account('52', 'ΤΡΑΠΕΖΕΣ-ΔΑΝΕΙΑ')
        self.add_account('53', 'ΠΙΣΤΩΤΕΣ ΔΙΑΦΟΡΟΙ')
        self.add_account('54', 'ΦΟΡΟΙ-ΤΕΛΗ')
        self.add_account('54.00', 'ΦΠΑ')
        self.add_account('54.00.20', 'ΦΠΑ ΑΓΟΡΩΝ ΕΜΠΟΡΕΥΜΑΤΩΝ')
        self.add_account('54.00.24', 'ΦΠΑ ΑΓΟΡΩΝ Α&Β ΥΛΩΝ')
        self.add_account('54.00.25', 'ΦΠΑ ΑΓΟΡΩΝ ΑΝΑΛΩΣΙΜΩΝ')
        self.add_account('54.00.29', 'ΦΠΑ ΕΞΟΔΩΝ')
        self.add_account('54.00.70', 'ΦΠΑ ΠΩΛΗΣΕΩΝ ΕΜΠΟΡΕΥΜΑΤΩΝ')
        self.add_account('54.00.71', 'ΦΠΑ ΠΩΛΗΣΕΩΝ ΠΡΟΪΟΝΤΩΝ')
        self.add_account('54.00.73', 'ΦΠΑ ΠΩΛΗΣΕΩΝ ΠΑΡΟΧΗΣ ΥΠΗΡΕΣΙΩΝ')
        self.add_account('54.00.99', 'ΦΠΑ ΛΜΟΣ ΕΚΚΑΘΑΡΙΣΗΣ')
        self.add_account('55', 'ΑΣΦΑΛΙΣΤΙΚΟΙ ΟΡΓΑΝΙΣΜΟΙ')
        self.add_account('60', 'ΑΜΟΙΒΕΣ & ΕΞΟΔΑ ΠΡΟΣΩΠΙΚΟΥ')
        self.add_account('61', 'ΑΜΟΙΒΕΣ & ΕΞΟΔΑ ΤΡΙΤΩΝ')
        self.add_account('62', 'ΠΑΡΟΧΕΣ ΤΡΙΤΩΝ')
        self.add_account('63', 'ΦΟΡΟΙ-ΤΕΛΗ')
        self.add_account('64', 'ΔΙΑΦΟΡΑ ΕΞΟΔΑ')
        self.add_account('64.00', 'ΕΞΟΔΑ ΜΕΤΑΦΟΡΩΝ')
        self.add_account('64.01', 'ΕΞΟΔΑ ΤΑΞΕΙΔΙΩΝ')
        self.add_account('64.03', 'ΕΞΟΔΑ ΕΚΘΕΣΕΩΝ-ΕΠΙΔΕΙΞΕΩΝ')
        self.add_account('64.04', 'ΕΙΔΙΚΑ ΕΞΟΔΑ ΠΡΟΩΘΗΣΗΣ ΕΞΑΓΩΓΩΝ')
        self.add_account('64.05', 'ΣΥΝΔΡΟΜΕΣ-ΕΙΣΦΟΡΕΣ')
        self.add_account('64.06', 'ΔΩΡΕΕΣ-ΕΠΙΧΟΡΗΓΗΣΕΙΣ')
        self.add_account('64.07', 'ΕΝΤΥΠΑ & ΓΡΑΦΙΚΗ ΥΛΗ')
        self.add_account('64.08', 'ΥΛΙΚΑ ΑΜΕΣΗΣ ΑΝΑΛΩΣΗΣ')
        self.add_account('64.09', 'ΕΞΟΔΑ ΔΗΜΟΣΙΕΥΣΕΩΝ')
        self.add_account('64.10', 'ΕΞΟΔΑ ΣΥΜΜΕΤΟΧΩΝ & ΧΡΕΟΓΡΑΦΩΝ')
        self.add_account('65', 'ΤΟΚΟΙ & ΣΥΝΑΦΗ ΕΞΟΔΑ')
        self.add_account('66', 'ΑΠΟΣΒΕΣΕΙΣ')
        self.add_account('70', 'ΠΩΛΗΣΕΙΣ ΕΜΠΟΡΕΥΜΑΤΩΝ')
        self.add_account('71', 'ΠΩΛΗΣΕΙΣ ΠΡΟΪΟΝΤΩΝ')
        self.add_account('73', 'ΠΑΡΟΧΗ ΥΠΗΡΕΣΙΩΝ')

    def add_account_object(self, account: Account, force_update_name: bool = False) -> None:
        if not isinstance(account, Account):
            raise ValueError(f"account parameter is not Account object")
        if account.code in self.accounts:
            if account.name == '':
                return
            if force_update_name:
                self.accounts[account.code] = account
            elif self.accounts[account.code].name == '':
                self.accounts[account.code] = account
            elif account.name != self.accounts[account.code].name:
                raise ValueError(
                    f"There is already account:  with same code "
                    f"but with different name"
                )
        else:
            self.accounts[account.code] = account

    def add_account(self, code: str, name: str, force_update_name: bool = False) -> None:
        self.add_account_object(Account(code, name), force_update_name)

    def add_accounts_from_dict(self, acc_dict):
        for key, val in acc_dict.items():
            self.add_account(key, val)

    def find_by_code(self, code_part: str) -> list:
        found = []
        for account in self.accounts.values():
            if code_part in account.code:
                found.append(account)
        return found

    def account_name(self, code: str) -> str:
        for account in self.accounts.values():
            if code == account.code:
                return account.name
            else:
                pass
        return ''

    def closest_name(self, code: str) -> str:
        """
        Get closest possible name for the account
        """
        levels = levels_reverse(code)
        for level in levels:
            if level in self.accounts:
                return self.accounts[level].name
        return ''

    def find_by_name(self, name_part: str) -> list:
        found = []
        for account in self.accounts.values():
            if name_part in account.name:
                found.append(account)
        return found

    def find_by_any(self, any_part: list) -> list:
        found = []
        for account in self.accounts.values():
            if any_part in account.name or any_part in account.code:
                found.append(account)
        return found

    def without_name(self):
        fli = []
        for key in sorted(self.accounts):
            if self.accounts[key].name == '':
                fli.append(key)
        return fli

    def __str__(self):
        return '\n'.join([i.__str__() for i in self.accounts.values()])
