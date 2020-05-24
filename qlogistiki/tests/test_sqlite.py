from os import name
from unittest import TestCase
from collections import namedtuple
from qlogistiki.sqlite import DataManager


class TestSqlite(TestCase):
    def setUp(self) -> None:
        self.db = DataManager()
        self.db.create_table('erg', {'epo': 'TEXT', 'ono': 'TEXT'})
        self.db.add('erg', {'epo': 'Laz', 'ono': 'Ted'})
        self.db.add('erg', {'epo': 'Laz', 'ono': 'Kon'})
        self.db.add('erg', {'epo': 'Dazea', 'ono': 'Popi'})
        self.db.create_md(
            'trn',
            'trnd',
            {
                'date': 'DATE',
                'par': 'TEXT NOT NULL',
                'per': 'TEXT NOT NULL',
                'afm': 'TEXT'
            },
            {
                'acc': 'TEXT NOT NULL',
                'val': 'NUMERIC NOT NULL DEFAULT 0'
            }
        )

    def tearDown(self) -> None:
        # self.db.close()
        pass

    def test_md(self):
        self.db.add_md(
            'trn',
            'trnd',
            {
                'master': {'date': '2019-01-15', 'par': 'TDA35', 'per': 'test'},
                'detail': [
                    {'acc': '38.00.00', 'val': 100},
                    {'acc': '30.00.00', 'val': 100}
                ]
            }
        )
        self.db.add_md(
            'trn',
            'trnd',
            {
                'master': {'date': '2019-01-16', 'par': 'TDA36', 'per': 'test2'},
                'detail': [
                    {'acc': '20.00.24', 'val': 100},
                    {'acc': '54.00.24', 'val': 24},
                    {'acc': '50.00.00', 'val': -124}
                ]
            }
        )
        # print(self.db.select_md('trn', 'trnd', 2))

    def test_select(self):
        Row = namedtuple('Row', 'id epo ono')
        vals = [
            Row(id=1, epo='Laz', ono='Ted'),
            Row(id=2, epo='Laz', ono='Kon'),
            Row(id=3, epo='Dazea', ono='Popi')
        ]
        val2 = [
            Row(id=1, epo='Laz', ono='Ted'),
            Row(id=3, epo='Dazea', ono='Popi')
        ]

        data_all = self.db.select('erg').fetchall()
        self.assertEqual(data_all, vals)

        data_one = self.db.select('erg', {'id': 2}).fetchone()
        self.assertEqual(data_one, Row(2, 'Laz', 'Kon'))

        self.assertTrue(self.db.delete('erg', {'id': 2}))

        self.assertEqual(self.db.lastrowid, 3)

    def test_attach_function(self):
        def grup(txtval):
            """Trasforms a string to uppercase special for Greek comparison
            """
            ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊΪκλμνξοόΌπρσςτυύϋΰΎΫφχψωώΏ"
            ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΥΥΥΦΧΨΩΩΩ"
            adi = dict(zip(ar1, ar2))
            return ''.join([adi.get(letter, letter.upper()) for letter in txtval])

        self.db.attach_function(grup)

        sql = 'SELECT grup(epo) as cepo FROM erg WHERE id < 3'
        Epo = namedtuple('Epo', 'cepo')
        data = self.db.sql(sql).fetchall()
        self.assertEqual(data, [Epo(cepo='LAZ'), Epo(cepo='LAZ')])

        self.db.add('erg', {'epo': 'Λάζαρος', 'ono': 'Θεόδωρος'})

        sql2 = 'SELECT GRUP(epo) as cepo FROM erg WHERE id=4'
        self.assertEqual(self.db.sql(sql2).fetchone(), Epo('ΛΑΖΑΡΟΣ'))

    def test_update(self):
        Row = namedtuple('Row', 'id epo ono')
        er1 = Row(1, 'Laz', 'Teddyboy')
        self.db.update('erg', {'ono': 'Teddyboy'}, 1)
        self.assertEqual(self.db.select('erg', {'id': 1}).fetchone(), er1)
