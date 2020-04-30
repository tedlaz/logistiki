"""Module recordset"""
import sqlite3


class Recordset:
    def __init__(self, headers, column_types, column_aligment, typ, data=None):
        self.headers = headers
        self.ctypes = column_types
        self.calign = column_aligment
        self.data = data if data else []
        self.typ = typ
        self.db = ''

    def new_row(self, obj):
        if isinstance(obj, self.typ):
            self.data.append(obj)
        else:
            raise ValueError(f'object {obj} is not of type {self.typ}')

    def add_may_rows(self, listofobj):
        self.data += listofobj

    def columns_size(self):
        return len(self.headers)

    def rows_size(self):
        return len(self.data)
