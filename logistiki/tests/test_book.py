from unittest import TestCase
from logistiki.book import Book


class TestsBook(TestCase):
    def test__adding_accounts(self):
        ali = {
            '20.00.024': 'Αγορές εμπ.',
            '54.00.224': 'ΦΠΑ αγ.εμπ 24%',
            '13.00.000': '',
            '10.00.000': ''
        }
        b1 = Book('book1')
        b1.accounts.add_accounts_from_dict(ali)
        self.assertEqual(b1.accounts.without_name(),
                         ['10.00.000', '13.00.000'])
        trans = [
            {
                'date': '2020-04-01', 'par': 'ΤΔΑ4', 'per': 'Δοκιμή τεστ1',
                'afm': '123123123',
                'lines': [
                    {'account': '20.00.013', 'typ': 1, 'value': 100},
                    {'account': '54.00.213', 'typ': 1, 'value': 13},
                    {'account': '50.00.001', 'typ': 2, 'value': 113},
                ]
            },
            {
                'date': '2020-01-01', 'par': 'ΤΔΑ3', 'per': 'Δοκιμή τεστ2',
                'afm': '123123123',
                'lines': [
                    {'account': '20.00.013', 'typ': 1, 'value': 100},
                    {'account': '54.00.213', 'typ': 1, 'value': 13},
                    {'account': '50.00.001', 'typ': 2, 'value': 113},
                ]
            }
        ]
        b1.add_transactions_from_list(trans)
        # print(b1.kartella('20.00', '2020-03-01', '2020-12-31'))
        print(b1.delta('5'))
