import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
from collections import namedtuple


class NoRecordFound(Exception):
    pass


def namedtuple_factory(cursor, row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


class Sqlite:
    def __init__(self, dbf=None):
        self.db = dbf
        self.connection = None
        self.lastrowid = 0

    def connect(self):
        if self.connection:
            return
        if self.db is None:
            self.db = ':memory:'
        try:
            self.connection = sqlite3.connect(self.db)
        except Exception as e:
            print(e)

    def attach_function(self, function):
        fname = function.__name__
        argno = function.__code__.co_argcount  # Number of arguments
        if self.connection:
            self.connection.create_function(fname, argno, function)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def create(self, sql):
        self.connect()
        try:
            self.connection.execute(sql)
        except OperationalError as e:
            print(e)

    def insert(self, sql):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            self.lastrowid = cursor.lastrowid
            cursor.close()
            return self.lastrowid
        except OperationalError as e:
            print(e)

    def update(self, sql):
        self.connect()
        try:
            self.connection.execute(sql)
            self.connection.commit()
        except OperationalError as e:
            print(e)

    def delete_table_id(self, table, id_):
        sql = f"DELETE FROM {table} WHERE id={id_};"
        self.select_one(sql)
        return True

    def select_one(self, sql):
        self.connection.row_factory = namedtuple_factory
        cursor = self.connection.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            return result
        return None

    def select_all(self, sql):
        self.connection.row_factory = namedtuple_factory
        cursor = self.connection.execute(sql)
        result = cursor.fetchall()
        if result is not None:
            return result
        return None

    def select_table_all(self, table):
        sql = f'SELECT * FROM {table};'
        return self.select_all(sql)

    def select_table_id(self, table, id_):
        sql = f'SELECT * FROM {table} WHERE id={id_};'
        return self.select_one(sql)
