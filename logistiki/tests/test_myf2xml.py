import os
from unittest import TestCase
from logistiki.myf2xml import create_xml


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestsMyf2xml(TestCase):
    def test_001(self):
        data = {
            'action': 'replace',
            'co': {
                'afm': '123123123', 'month': '12', 'year': '2019', 'branch': ''
            },
            'grevenues': [
                {'afm': '111222333', 'amount': '100,00', 'tax': '24,00',
                 'note': 'normal', 'invoices': 2, 'date': '2019-12-31'},
                {'afm': '111222444', 'amount': '200,00', 'tax': '48,00',
                 'note': 'normal', 'invoices': 5, 'date': '2019-12-31'},
                {'afm': '111222444', 'amount': '100,00', 'tax': '24,00',
                 'note': 'credit', 'invoices': 1, 'date': '2019-12-31'}
            ],
            'gexpenses': [
                {'afm': '111222333', 'amount': '100,00', 'tax': '24,00',
                 'note': 'normal', 'invoices': 12, 'date': '2019-12-31',
                 'nonObl': 0},
                {'afm': '111111333', 'amount': '325,68', 'tax': '68,34',
                 'note': 'normal', 'invoices': 15, 'date': '2019-12-31',
                 'nonObl': 0}
            ],
            'gcash': [
                {'tamNo': '', 'amount': '100,00',
                    'tax': '24,00', 'date': '2019-12-31'}
            ],
            'oexpenses': {
                'amount': '12344,56', 'tax': '4326,44', 'date': '2019-12-31'
            }
        }
        xmld = create_xml(data)
        xmlfile = os.path.join(dir_path, 'test_myf2xml.xml')
        xml_from_file = ''
        with open(xmlfile) as fil:
            xml_from_file = fil.read()
        self.assertEqual(xmld, xml_from_file)
