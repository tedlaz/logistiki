import os
from qlogistiki.book import Book
from qlogistiki.parser_text import parse

dir_path = os.path.dirname(os.path.realpath(__file__))
bfile = os.path.join(dir_path, "booktst.txt")


def test_book_creation():
    b01 = b01 = Book(*parse(bfile))
    print(b01.arthro_anoigmatos())
