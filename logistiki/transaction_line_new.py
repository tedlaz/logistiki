from decimal import Decimal
from typing import TypeVar
from logsitiki.debit_credit import DebitCredit as DeCre

TLine = TypeVar("TLine", bound="TransactionLine")
Numeric = TypeVar('Numeric', int, float, Decimal, str)


class TransactionLine:
    def __init__(self, code: str, typ: int, value: Numeric) -> None:
        self.code = code
        self.decre = DeCre(typ, value)

    def __repr__(self):
        return f"TLine(code='{self.code}', decre={self.decre})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TransactionLine):
            return NotImplemented
        if self.code != other.code:
            return False
        return True if self.decre.delta == other.decre.delta else False


if __name__ == '__main__':
    l1 = TransactionLine('24.00.013', 1, 102.34)
    print(l1)
    print(l1.decre * 10)
