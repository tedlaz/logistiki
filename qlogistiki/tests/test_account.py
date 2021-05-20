from qlogistiki.account import Account


def test_acc_tree():
    acc = Account("Aa.Bb.Cc")
    assert acc.tree == ["Aa", "Aa.Bb", "Aa.Bb.Cc"]
    assert acc.tree_reversed == ["Aa.Bb.Cc", "Aa.Bb", "Aa"]
