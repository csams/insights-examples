from contextlib import contextmanager
from MySQLdb import connect, cursors

from insights.core.context import HostContext
from insights.core.plugins import datasource


class Connection(object):
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


class MysqlConnection(Connection):
    host = None
    port = None
    user = None
    passwd = None
    db = None
    read_default_file = None
    timeout = 3

    def __init__(self, broker=None):
        with self.connection() as con:
            cursor = con.cursor()
            cursor.execute("select VERSION()")
            self.version = cursor.fetchone()

    def _connect_options(self):
        result = {}
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
            return connect(read_default_file=self.read_default_file)
        return connect(connect_timeout=self.timeout, **self._connect_options())

    def query(self, sql):
        with self.connection() as con:
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()


class sql_query(object):
    def __init__(self, con, sql, context=HostContext):
        self.con = con
        self.context = context
        self.sql = sql
        self.__name__ = self.__class__.__name__
        datasource(con, context)(self)

    def __call__(self, broker):
        con = broker[self.con]
        return con.query(self.sql)
