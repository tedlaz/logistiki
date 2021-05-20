from qlogistiki.data_manager_abstract import AbstractDataManager
from qlogistiki import sqlite


class DataManager(AbstractDataManager):
    def __init__(self, dbf=None):
        self.db = sqlite.DataManager(dbf)
        self.db.create_table(
            "bookmarks",
            {
                "title": "TEXT NOT NULL",
                "url": "TEXT NOT NULL",
                "notes": "TEXT",
                "date_added": "TEXT NOT NULL",
            },
        )
        self.lastrowid = 0

    def create(self, data):
        self.db.add("bookmarks", data)
        self.lastrowid = self.db.lastrowid

    def read(self, order_by):
        data = self.db.select("bookmarks", order_by=order_by).fetchall()
        return data

    def update(self, data):
        pass

    def delete(self, id_):
        self.db.delete("bookmarks", {"id": id_})

    def make_permanent(self):
        pass
