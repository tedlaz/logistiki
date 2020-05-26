from collections import namedtuple
from operator import attrgetter
from qlogistiki.data_manager_abstract import AbstractDataManager

Tdata = namedtuple('Tdata', 'id title url notes date_added')


class DataManager(AbstractDataManager):

    def __init__(self, file_name='test.txt'):
        # {r.id:5} {r.title:20} {r.url} {r.notes}
        self.data = {}
        self.filename = file_name
        id_ = 0
        try:
            with open(file_name, encoding='utf8') as fil:
                for line in fil.readlines():
                    id_, title, url, notes, date_added = line.strip().split('|')
                    id_ = int(id_)
                    self.data[id_] = Tdata(id_, title, url, notes, date_added)
        except Exception:
            pass
        self.lastrowid = id_

    def create(self, data):
        self.lastrowid += 1
        self.data[self.lastrowid] = Tdata(
            self.lastrowid,
            data['title'],
            data['url'],
            data['notes'],
            data['date_added']
        )

    def read(self, order_by):
        data = sorted(self.data.values(), key=attrgetter(order_by))
        return data

    def update(self, data):
        pass

    def delete(self, id_):
        del self.data[id_]

    def make_permanent(self):
        text_lines = ''
        for lin in self.data.values():
            text_lines += f'{lin.id}|{lin.title}|{lin.url}|{lin.notes}|{lin.date_added}\n'
        with open(self.filename, 'w', encoding='utf8') as fil:
            fil.write(text_lines)
