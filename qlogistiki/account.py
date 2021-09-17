"""
Class Account
"""


class Account:
    splitter = "."
    __slots__ = [
        "name",
    ]

    def __init__(self, name):
        self.name = name

    @property
    def tree(self) -> list:
        spl = self.name.split(self.splitter)
        lvls = [self.splitter.join(spl[: i + 1]) for i, _ in enumerate(spl)]
        return lvls

    @property
    def tree_reversed(self) -> list:
        lvls = self.tree
        lvls.reverse()
        return lvls

    def __repr__(self) -> str:
        return f"Account(name={self.name!r})"

    def __str__(self) -> str:
        return f"{self.name}"

    def __format__(self, format_spec) -> str:
        return f"{self.name:{format_spec}}"
