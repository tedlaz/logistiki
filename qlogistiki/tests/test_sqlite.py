from os import name
from unittest import TestCase
from collections import namedtuple
from qlogistiki.sqlite import Sqlite


class TestSqlite(TestCase):
    def setUp(self) -> None:
        self.db = Sqlite()
        self.db.create(
            "CREATE TABLE erg(id INTEGER PRIMARY KEY, epo TEXT, ono TEXT);")
        self.db.insert("INSERT INTO erg (epo, ono) VALUES('Laz', 'Ted');")
        self.db.insert("INSERT INTO erg (epo, ono) VALUES('Laz', 'Kon');")
        self.db.insert("INSERT INTO erg (epo, ono) VALUES('Dazea', 'Popi');")

    def tearDown(self) -> None:
        self.db.disconnect()

    def test_001(self):
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
        self.assertEqual(self.db.select_all("SELECT * FROM erg"), vals)
        self.assertEqual(self.db.select_one(
            "SELECT * FROM erg where id=2"), Row(2, 'Laz', 'Kon'))
        self.assertEqual(self.db.select_table_all('erg'), vals)
        self.assertEqual(
            self.db.select_table_id('erg', 2),
            Row(2, 'Laz', 'Kon')
        )
        self.assertTrue(self.db.delete_table_id('erg', 2))
        self.assertEqual(self.db.select_table_all('erg'), val2)
        self.assertEqual(self.db.lastrowid, 3)

    def test_002(self):
        def grup(txtval):
            """Trasforms a string to uppercase special for Greek comparison
            """
            ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊΪκλμνξοόΌπρσςτυύϋΰΎΫφχψωώΏ"
            ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΥΥΥΦΧΨΩΩΩ"
            adi = dict(zip(ar1, ar2))
            return ''.join([adi.get(letter, letter.upper()) for letter in txtval])

        self.db.attach_function(grup)
        sql = 'SELECT grup(epo) as cepo FROM erg'
        Epo = namedtuple('Epo', 'cepo')
        self.assertEqual(
            self.db.select_all(sql),
            [Epo(cepo='LAZ'), Epo(cepo='LAZ'), Epo(cepo='DAZEA')]
        )
        self.db.insert(
            "INSERT INTO erg (epo, ono) VALUES('Λάζαρος', 'Θεόδωρος');")
        sql2 = 'SELECT GRUP(epo) as cepo FROM erg WHERE id=4'
        self.assertEqual(self.db.select_one(sql2), Epo('ΛΑΖΑΡΟΣ'))
