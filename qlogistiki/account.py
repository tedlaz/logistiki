"""
Class Account
"""


class Account():
    splitter = '.'
    __slots__ = ['name', ]

    def __init__(self, name):
        self.name = name

    @property
    def tree(self):
        spl = self.name.split(self.splitter)
        lvls = [self.splitter.join(spl[: i + 1]) for i, _ in enumerate(spl)]
        return lvls

    @property
    def tree_reversed(self):
        lvls = self.tree
        lvls.reverse()
        return lvls

    def __repr__(self):
        return f'Account(name={self.name!r})'
