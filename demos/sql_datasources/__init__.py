"""
The base Connection classes that provide query facilities against Mysql and
Postgres databases.
"""
from contextlib import contextmanager
from insights.core.context import HostContext
from insights.core.plugins import datasource

import MySQLdb
import psycopg2
import psycopg2.extras  # provides the RealDictCursor


class Connection(object):
    """
    Provides context managers for operating within a live connection and a
    transaction.
    """
    host = None
    port = None
    user = None
    passwd = None
    db = None

    def __init__(self, broker=None):
        with self.connection():
            pass

    def connect(self):
        raise NotImplemented()

    @contextmanager
    def transaction(self):
        with self.connection() as con:
            try:
                con.begin()
                yield con
            except:
                con.rollback()
            else:
                con.commit()

    @contextmanager
    def connection(self):
        con = None
        try:
            con = self.connect()
            yield con
        finally:
            if con:
                con.close()

    def query(self, sql):
        with self.connection() as con:
            cursor = con.cursor()
            cursor.execute(sql)
            return cursor.fetchall()


class MysqlConnection(Connection):
    read_default_file = None
    timeout = 3

    def _connect_options(self):
        result = {"cursorclass": MySQLdb.cursors.DictCursor}
        if self.host:
            result["host"] = self.host
        if self.port:
            result["port"] = self.port
        if self.user:
            result["user"] = self.user
        if self.passwd:
            result["passwd"] = self.passwd
        if self.db:
            result["db"] = self.db
        return result

    def connect(self):
        if self.read_default_file:
            return MySQLdb.connect(read_default_file=self.read_default_file, cursorclass=MySQLdb.cursors.DictCursor)
        return MySQLdb.connect(connect_timeout=self.timeout, **self._connect_options())


class PostgresConnection(Connection):
    def _connect_options(self):
        result = {}
        if self.host:
            result["host"] = self.host
        if self.db:
            result["dbname"] = self.db
        if self.port:
            result["port"] = self.port
        if self.user:
            result["user"] = self.user
        if self.passwd:
            result["password"] = self.passwd
        return result

    def connect(self):
        cur = psycopg2.extras.RealDictCursor
        return psycopg2.connect(cursor_factory=cur, **self._connect_options())


class sql_query(object):
    """
    A helper class for running sql queries against a connection. Will execute
    only if given a valid connection within a HostContext.
    """
    def __init__(self, con, sql, context=HostContext):
        self.con = con
        self.context = context
        self.sql = sql
        self.__name__ = self.__class__.__name__
        datasource(con, context)(self)

    def __call__(self, broker):
        return broker[self.con].query(self.sql)
