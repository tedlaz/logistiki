import sys
import os
from datetime import datetime
from qlogistiki.sqlite import DataManager

db = DataManager()


class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table(
            'bookmarks',
            {
                'title': 'TEXT NOT NULL',
                'url': 'TEXT NOT NULL',
                'notes': 'TEXT',
                'date_added': 'TEXT NOT NULL'
            }
        )


class AddBookmarkCommand:
    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return f'Bookmark No {db.lastrowid} added!'


class ListBookmarksCommand:
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        data = db.select('bookmarks', order_by=self.order_by).fetchall()
        return '\n'.join(f'{r.id:5} {r.title:20} {r.url} {r.notes}' for r in data)


class EditBookmarkCommand:
    def execute(self, data):
        db.update('bookmarks', data, 12)


class DeleteBookmarkCommand:
    def execute(self, id_):
        db.delete('bookmarks', {'id': id_})
        return f'Bookmark with id={id_} deleted'


class QuitCommand:
    def execute(self):
        sys.exit()


class Option:
    def __init__(self, name: str, command, prep_call=None) -> None:
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        msg = self.command.execute(data) if data else self.command.execute()
        print(msg)

    def __str__(self):
        return self.name


def print_options(options):
    for key, val in options.items():
        print(f'({key}) {val}')
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('invalid choice')
        choice = input('Choose an option: ')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False),
    }


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a Bookmar id to delete')


def get_bookmark_id_for_editing():
    return get_user_input('Enter a bookmark id for editing')


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def loop():
    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()
    input("Press Enter to continue...")


if __name__ == '__main__':
    print('welcome to Bark!')
    CreateBookmarksTableCommand().execute()
    options = {
        'A': Option('Add a bookmark', AddBookmarkCommand(), get_new_bookmark_data),
        'B': Option('List Bookmarks by date', ListBookmarksCommand()),
        'T': Option('List Bookmarks by title', ListBookmarksCommand('title')),
        'E': Option('Edit Bookmark', EditBookmarkCommand(), get_bookmark_id_for_editing),
        'D': Option('Delete a Bookmark', DeleteBookmarkCommand(), get_bookmark_id_for_deletion),
        'Q': Option('Quit', QuitCommand())
    }
    while True:
        loop()
