from decimal import Decimal
from typing import TypeVar
from logistiki.udec import dec, dec2gr


TDebitCredit = TypeVar("TDebitCredit", bound="DebitCredit")


class DebitCredit:
    def __init__(self, debit_credit: int = 1, value=0) -> None:
        self.dc = 2 if debit_credit > 1 else 1
        self.value = dec(value)

    @classmethod
    def new_by_dc(cls, debit=0, credit=0) -> TDebitCredit:
        """
        Create a new DebitCredit object by debit, credit values
        """
        if debit == 0:
            return cls(2, dec(credit))
        if credit == 0:
            return cls(1, debit)
        ypol = dec(debit - credit)
        return cls(2, -ypol) if ypol < 0 else cls(1, ypol)

    @property
    def real_dc(self):
        return 2 if self.delta < 0 else 1

    @property
    def value_positive(self) -> Decimal:
        return abs(self.value)

    @property
    def debit(self) -> Decimal:
        """Get the debit value"""
        return self.value if self.dc == 1 else dec(0)

    @property
    def debit_positive(self) -> Decimal:
        return dec(0) if self.delta < 0 else self.delta

    @property
    def debit_negative(self) -> Decimal:
        return self.delta if self.delta < 0 else dec(0)

    @property
    def xreosi(self) -> str:
        return dec2gr(self.debit)

    @property
    def xreosi_positive(self) -> str:
        return dec2gr(self.debit_positive)

    @property
    def xreosi_negative(self) -> str:
        return dec2gr(self.debit_negative)

    @property
    def credit(self) -> Decimal:
        """Get the credit value"""
        return self.value if self.dc == 2 else dec(0)

    @property
    def credit_positive(self) -> Decimal:
        return - self.delta if self.delta < 0 else dec(0)

    @property
    def credit_negative(self) -> Decimal:
        return dec(0) if self.delta < 0 else -self.delta

    @property
    def pistosi(self) -> str:
        return dec2gr(self.credit)

    @property
    def pistosi_positive(self) -> str:
        return dec2gr(self.credit_positive)

    @property
    def pistosi_negative(self) -> str:
        return dec2gr(self.credit_negative)

    @property
    def delta(self) -> Decimal:
        """Get the difference (debit - credit) value """
        return self.value if self.dc == 1 else -self.value

    @property
    def ypoloipo(self) -> str:
        return dec2gr(self.delta)

    def positived(self) -> TDebitCredit:
        """
        Create a new DebitCredit object with positive self.value
        """
        delta = self.delta
        return DebitCredit(2, -delta) if delta < 0 else DebitCredit(1, delta)

    def negatived(self) -> TDebitCredit:
        """
        Create a new DebitCredit object with negative self.value
        """
        delta = self.delta
        return DebitCredit(1, delta) if delta < 0 else DebitCredit(2, -delta)

    def __repr__(self):
        return f"DeCre(dc={self.dc}, value={self.value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DebitCredit):
            return NotImplemented
        return True if self.delta == other.delta else False

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DebitCredit):
            return NotImplemented
        return self.delta < other.delta

    def __neg__(self) -> TDebitCredit:
        return DebitCredit(self.dc, -self.value)

    def __add__(self, other: object) -> TDebitCredit:
        if not isinstance(other, DebitCredit):
            return NotImplemented
        val = self.delta + other.delta
        return DebitCredit(2, -val) if val < 0 else DebitCredit(1, val)

    def __sub__(self, other: object) -> TDebitCredit:
        if not isinstance(other, DebitCredit):
            return NotImplemented
        val = self.delta - other.delta
        return DebitCredit(2, -val) if val < 0 else DebitCredit(1, val)

    def __mul__(self, anumber: object) -> TDebitCredit:
        fval = dec(anumber)
        return DebitCredit(self.dc, dec(self.value * fval))

    def __truediv__(self, anumber) -> TDebitCredit:
        fval = dec(anumber)
        return DebitCredit(self.dc, dec(self.value / fval))
