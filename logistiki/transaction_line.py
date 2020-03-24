from decimal import Decimal
from hashlib import sha1
from logistiki.account import Account
from typing import TypeVar
from logistiki.udec import dec


TLine = TypeVar("TLine", bound="TransactionLine")


class TransactionLine:
    """Transaction detail line containing account typ and value"""

    def __init__(self, account: Account, typ: int, value: Decimal) -> None:
        if not isinstance(account, Account):
            raise ValueError(f"Parameter account({account}) is not Account")
        self.account = account
        self.typ = typ
        self.value = dec(value)

    @classmethod
    def new_by_code(cls, account_code, typ, value):
        account = Account(account_code, '')
        return cls(account, typ, dec(value))

    @classmethod
    def new_by_code_name(cls, account_code, account_name, typ, value) -> TLine:
        account = Account(account_code, account_name)
        return cls(account, typ, dec(value))

    @classmethod
    def from_dict(cls, adict: dict) -> TLine:
        account = Account(adict['account-code'], adict['account-name'])
        return cls(account, adict['typ'], adict['value'])

    def normalize(self) -> None:
        """
        Normalizes current object
        """
        if self.value < 0:
            self.value = -self.value
            if self.typ == 1:
                self.typ = 2
            else:
                self.typ = 1

    @property
    def new_object(self) -> TLine:
        return TransactionLine(self.account, self.typ, self.value)

    @property
    def new_normal(self) -> TLine:
        """
        Return a new normalized Tline object
        """
        typ = self.typ
        value = self.value
        if value < 0:
            value = -value
            if typ == 1:
                typ = 2
            else:
                typ = 1
        return TransactionLine(self.account, typ, value)

    @property
    def new_negative(self) -> TLine:
        if self.typ == 1:
            typ = 2
        else:
            typ = 1
        return TransactionLine(self.account, typ, -self.value)

    @property
    def flat_value(self):
        """
        Επιστρέφει θετικό αν τυπος χρέωση αρνητικό διαφορετικά
        πχ αν έχουμε ('38.00.00', 1, 15.32) επιστρέφει 15.32
           αν έχουμε ('38.03.00', 2, 57.44) επιστρέφει -57.44
        """
        if self.typ == 1:
            return self.value
        return -self.value

    @property
    def to_dict(self) -> dict:
        return {'account': self.account.code, 'typ': self.typ, 'value': self.value}

    @property
    def debit(self) -> Decimal:
        if self.typ == 1:
            return self.value
        return dec(0)

    @property
    def credit(self) -> Decimal:
        if self.typ != 1:
            return self.value
        return dec(0)

    @property
    def sha1(self) -> str:
        """Create sha1 of the class according to self._str_byte"""
        ash1 = sha1()
        ash1.update(self._str_byte)
        return ash1.hexdigest()

    @property
    def _str_byte(self) -> bytes:
        """String representation of Tline transformed to bytes"""
        ast = f"{self.account.code}{self.typ}{self.value}"
        return ast.encode()

    def __repr__(self):
        return f"TransactionLine(account='{self.account}', typ={self.typ}, value={self.value})"

    def __str_for_comparison(self):
        return f'{self.account.code}{self.typ}{self.value}'

    def __str__(self):
        return f"{self.account.code:<15}{self.debit:>14.2f}{self.credit:>14.2f}"

    def __eq__(self, other: object) -> bool:
        """Overrides the default implementation"""
        if not isinstance(other, TransactionLine):
            return NotImplemented
        if self.account.code != other.account.code:
            return False
        if self.flat_value != other.flat_value:
            return False
        return True

    def __neg__(self) -> TLine:
        return TransactionLine(self.account, self.typ, -self.value)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TransactionLine):
            return NotImplemented
        return self.__str_for_comparison() < other.__str_for_comparison()

    def __mul__(self, anumber):
        fval = dec(anumber)
        return TransactionLine(self.account, self.typ, dec(self.value * fval))
