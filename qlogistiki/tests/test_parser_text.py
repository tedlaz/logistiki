import os
from qlogistiki.parser_text import parse

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_parser_text_001():
    book_data = os.path.join(dir_path, 'booktst.txt')
    afm, name, trans, valids, accounts, anoigma = parse(book_data)
    # print('\n', valids, trans[0])
    assert sum(accounts.values()) == 0
    # print(trans[0].lines[0].account.account_dict)
    # print(afm, name)
