import unittest
from qlogistiki import enterprise as ens


class TestEnterprise(unittest.TestCase):
    def test_ooo(self):
        en1 = ens.Enterprise('123123120', 'ΛΑΖΑΡΟΣ ΑΕ')
        pel1 = ens.CustomerGreece('111222333', 'Γεωργίου Απόστολος')
        # print(pel1, repr(pel1), pel1.partner_type)
