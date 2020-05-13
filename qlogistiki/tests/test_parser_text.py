import os
from unittest import TestCase

from qlogistiki.parser_text import parse

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestParser(TestCase):
    def test_001(self):
        book_data = os.path.join(dir_path, 'booktst.txt')
        afm, name, trans, valids, accounts = parse(book_data)
        # print('\n', valids, trans[0])
        self.assertEqual(sum(accounts.values()), 0)
        # print(trans[0].lines[0].account.account_dict)
        # print(afm, name)