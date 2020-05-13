import unittest
from qlogistiki.account import Account


class TestAccount(unittest.TestCase):
    def test_acc_tree(self):
        acc = Account('Aa.Bb.Cc')
        self.assertEqual(acc.tree, ['Aa', 'Aa.Bb', 'Aa.Bb.Cc'])
        self.assertEqual(acc.tree_reversed, ['Aa.Bb.Cc', 'Aa.Bb', 'Aa'])
