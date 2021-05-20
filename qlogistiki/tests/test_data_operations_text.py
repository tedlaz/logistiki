import os
from qlogistiki import data_operations_text as dot

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_001():
    bfile = os.path.join(dir_path, "booktst.txt")
    book = dot.load_from_text(bfile)
    btxt = dot.save_dummy(book)
    assert btxt.startswith("$ 111222333 Μαλακόπουλος ΕΠΕ")
    assert btxt[-16:-2] == "Μετρητά.Ταμείο"
