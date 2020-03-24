from unittest import TestCase
from logistiki.account import Account, AccountContainer, levels, levels_reverse


class TestsAccount(TestCase):
    def test_001(self):
        ac1 = Account('54.00.00.224', 'ΦΠΑ Αγορών 24%')
        self.assertEqual(ac1.levels, ('5', '54', '54.00',
                                      '54.00.00', '54.00.00.224'))
        self.assertTrue(ac1.is_fpa)
        self.assertFalse(ac1.is_ee)
        self.assertFalse(ac1.is_apotelesma)
        self.assertEqual(ac1.omada_name, 'ΥΠΟΧΡΕΩΣΕΙΣ')
        self.assertEqual(ac1.omada, 5)
        self.assertEqual(ac1.omada_default_typ, 2)

    def test_account_container(self):
        cont = AccountContainer()
        ac13 = Account('20.00.013', 'Αγορές εμπορευμάτων 13% ΦΠΑ')
        ac24 = Account('20.00.024', 'Αγορές εμπορευμάτων 24% ΦΠΑ')
        ac54 = Account('54.00', 'ΦΠΑ')
        cont.add_account_object(ac13)
        cont.add_account_object(ac24)
        cont.add_account_object(ac54)
        self.assertEqual(cont.find_by_code('54.01'), [])
        # self.assertEqual(cont.find_by_code('54.00'), [ac54])
        self.assertEqual(cont.find_by_code('20.00'), [ac13, ac24])

    def test_account_container_update(self):
        cont = AccountContainer()
        ac13 = Account('20.00.013', 'Αγορές εμπορευμάτων 13% ΦΠΑ')
        cont.add_account_object(ac13)
        cont.add_account('20.00.013', 'Δοκιμή', force_update_name=True)
        cont.add_account('20.00.013', '')

    def test_account_container_002(self):
        ali = {
            '20.00.024': 'Αγορές εμπ.',
            '54.00.224': 'ΦΠΑ αγ.εμπ 24%',
            '13.00.000': '',
            '10.00.000': ''
        }
        ac1 = AccountContainer()
        ac1.add_accounts_from_dict(ali)
        self.assertEqual(ac1.without_name(), ['10.00.000', '13.00.000'])

    def test_levels(self):
        print(levels('20.00.000'))
        print(levels_reverse('20.00.000'))
