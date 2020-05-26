from collections import namedtuple
from qlogistiki.sqlite import DataManager
import pytest


@pytest.fixture
def dbc():
    db = DataManager()
    db.create_table('erg', {'epo': 'TEXT', 'ono': 'TEXT'})
    db.add('erg', {'epo': 'Laz', 'ono': 'Ted'})
    db.add('erg', {'epo': 'Laz', 'ono': 'Kon'})
    db.add('erg', {'epo': 'Dazea', 'ono': 'Popi'})
    db.create_md(
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
    return db


def test_md(dbc):
    dbc.add_md(
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
    dbc.add_md(
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


def test_select(dbc):
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

    data_all = dbc.select('erg').fetchall()
    assert data_all == vals

    data_one = dbc.select('erg', {'id': 2}).fetchone()
    assert data_one == Row(2, 'Laz', 'Kon')
    assert dbc.delete('erg', {'id': 2})
    assert dbc.lastrowid == 3


def test_attach_function(dbc):
    def grup(txtval):
        """Trasforms a string to uppercase special for Greek comparison
        """
        ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊΪκλμνξοόΌπρσςτυύϋΰΎΫφχψωώΏ"
        ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΥΥΥΦΧΨΩΩΩ"
        adi = dict(zip(ar1, ar2))
        return ''.join([adi.get(letter, letter.upper()) for letter in txtval])

    dbc.attach_function(grup)

    sql = 'SELECT grup(epo) as cepo FROM erg WHERE id < 3'
    Epo = namedtuple('Epo', 'cepo')
    data = dbc.sql(sql).fetchall()
    assert data == [Epo(cepo='LAZ'), Epo(cepo='LAZ')]

    dbc.add('erg', {'epo': 'Λάζαρος', 'ono': 'Θεόδωρος'})

    sql2 = 'SELECT GRUP(epo) as cepo FROM erg WHERE id=4'
    assert dbc.sql(sql2).fetchone() == Epo('ΛΑΖΑΡΟΣ')


def test_update(dbc):
    Row = namedtuple('Row', 'id epo ono')
    er1 = Row(1, 'Laz', 'Teddyboy')
    dbc.update('erg', {'ono': 'Teddyboy'}, 1)
    assert dbc.select('erg', {'id': 1}).fetchone() == er1
