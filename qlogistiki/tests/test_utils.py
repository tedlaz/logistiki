from qlogistiki import utils as utl
from qlogistiki.utils import grup


def test_gr_num():
    assert utl.gr_num(1010.34) == '1.010,34'
    assert utl.gr_num(0) == '0   '
    assert utl.gr_num(123123.50) == '123.123,5 '
    assert utl.gr_num(-123123.50) == '-123.123,5 '
    assert utl.gr_num(.01) == '0,01'
    assert utl.gr_num(-.01) == '-0,01'
    assert utl.gr_num(.10) == '0,1 '
    assert utl.gr_num(-82.00) == '-82   '
    assert utl.gr_num('rt') == '0   '
    assert utl.gr_num(None) == '0   '


def test_account_tree():
    assert utl.account_tree('a.b.c') == ('a', 'a.b', 'a.b.c')
    assert utl.account_tree('a') == ('a',)
    assert utl.account_tree('') == ('',)
    assert utl.account_tree(1) == ('',)
    assert utl.account_tree('a.b', True) == ('a.b', 'a')


def test_grup():
    assert grup('ΐέάό') == 'ΙΕΑΟ'
    assert grup('Ίώνάς') == 'ΙΩΝΑΣ'
    assert grup('ϊίΫώrock123') == 'ΙΙΥΩROCK123'


def test_is_afm():
    assert utl.is_afm('094025817')
    assert not utl.is_afm('094025818')
    assert not utl.is_afm('0')
    assert not utl.is_afm('0940258179')
