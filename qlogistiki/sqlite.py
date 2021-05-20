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


class DataManager:
    def __init__(self, dbf=None):
        self.db = dbf
        self.connection = None
        self.lastrowid = 0

    def __del__(self):
        if self.connection:
            self.connection.close()

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def connect(self):
        if self.connection:
            return
        if self.db is None:
            self.db = ":memory:"
        try:
            self.connection = sqlite3.connect(self.db)
            self.connection.row_factory = namedtuple_factory
        except Exception as e:
            print(e)

    def attach_function(self, function):
        fname = function.__name__
        argno = function.__code__.co_argcount  # Number of arguments
        if self.connection:
            self.connection.create_function(fname, argno, function)

    def _execute(self, sql, parameters=None):
        self.connect()
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql, parameters or [])
            return cursor

    def create_table(self, table_name: str, columns: dict):
        columns_sql = [
            f"{column_name} {column_type}"
            for column_name, column_type in columns.items()
        ]
        id_sql = ["id INTEGER PRIMARY KEY"]
        sql_list = id_sql + columns_sql
        sql = f"CREATE TABLE IF NOT EXISTS {table_name}" f"({', '.join(sql_list)});"
        self._execute(sql)

    def add(self, table_name: str, data: dict) -> int:
        qmarks = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())
        sql = f"INSERT INTO {table_name} " f"({column_names}) " f"VALUES ({qmarks});"
        cursor = self._execute(sql, column_values)
        self.lastrowid = cursor.lastrowid
        return self.lastrowid

    def update(self, table_name: str, data: dict, id_: int):
        sql_columns = ", ".join([f"{column} = ?" for column in data.keys()])
        sql = f"UPDATE {table_name} " f"SET {sql_columns} " f"WHERE id={id_};"
        self._execute(sql, tuple(data.values()))

    def delete(self, table_name: str, criteria: dict):
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        sql = f"DELETE FROM {table_name} WHERE {delete_criteria};"
        self._execute(sql, tuple(criteria.values()))
        return True

    def select(self, table_name, criteria: dict = None, order_by: str = None):
        criteria = criteria or {}
        sql = f"SELECT * FROM {table_name}"

        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            sql_criteria = " AND ".join(placeholders)
            sql += f" WHERE {sql_criteria}"

        if order_by:
            sql += f" ORDER BY {order_by}"

        return self._execute(sql, tuple(criteria.values()))

    def create_md(self, master, detail, columns_master, columns_detail):
        self.create_table(master, columns_master)
        columns_detail[f"{master}_id"] = "INTEGER NOT NULL"
        self.create_table(detail, columns_detail)

    def select_md(self, master, detail, id_):
        sqlm = f"SELECT * from {master} WHERE id={id_};"
        sqld = f"SELECT * from {detail} WHERE {master}_id={id_};"
        data = {}
        data["master"] = self._execute(sqlm).fetchone()
        data["detail"] = self._execute(sqld).fetchall()
        return data

    def add_md(self, master, detail, data):
        lastid = self.add(master, data["master"])
        for det in data["detail"]:
            det[f"{master}_id"] = lastid
            self.add(detail, det)

    def update_md(self, master, detail, criteria):
        pass

    def sql(self, sql):
        """
        Execute plain sql
        """
        return self._execute(sql)
