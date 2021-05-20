import os
from qlogistiki.parser_text import parse
from qlogistiki.book import Book


def load_from_text(text_file):
    return Book(*parse(text_file))


def save2text(book, destination_file):
    if os.path.exists(destination_file):
        raise ValueError("file already exists")
    with open(destination_file, "w") as fil:
        fil.write(f"$ {book.afm} {book.company_name}\n")
        for trn in sorted(book.transactions):
            fil.write(trn.as_str())
            fil.write("\n")
    print(f"Book saved to {destination_file}")


def save_dummy(abook):
    txt = f"$ {abook.afm} {abook.company_name}\n"
    for trn in sorted(abook.transactions):
        txt += f"{trn.as_str()}\n"
    return txt
