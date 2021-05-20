from qlogistiki.utils import dec
from qlogistiki.account import Account
from qlogistiki.dec import Dec


class TransactionLine:
    __slots__ = ["account", "value", "sxolio"]

    def __init__(self, account, value, sxolio=""):
        self.account = Account(account)
        self.value = Dec(value)
        self.sxolio = sxolio.strip()

    @property
    def debit(self) -> Dec:
        if self.value > 0:
            return self.value
        return Dec(0)

    @property
    def credit(self) -> Dec:
        if self.value < 0:
            return -self.value
        return Dec(0)

    @property
    def delta(self) -> Dec:
        """For compatibility reasons only"""
        return self.value

    def __eq__(self, other):
        return (self.value == other.value) and (self.account.name == other.account.name)

    def __lt__(self, other):
        if self.account.name == other.account.name:
            return self.value < other.value
        return self.account.name < other.account.name

    def __mul__(self, number):
        return TransactionLine(self.account.name, self.value * number)

    def __rmul__(self, number):
        return TransactionLine(self.account.name, self.value * number)

    def __add__(self, other):
        if self.account.name != other.account.name:
            raise ValueError("For addition accounts must me the same")
        return TransactionLine(self.account.name, self.value + other.value)

    def __repr__(self):
        return (
            "TransactionLine(" f"account={self.account!r}, " f"value={self.value!r}" ")"
        )

    def __str__(self):
        return f"{self.account:<30} {self.debit:>14} {self.credit:>14}"
