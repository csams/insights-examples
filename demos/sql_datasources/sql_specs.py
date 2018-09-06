from functools import partial

from insights.core.plugins import datasource
from insights.core.spec_factory import SpecSet
from . import sql_query, MysqlConnection


@datasource()
class LocalTestDb(MysqlConnection):
    db = "test"


sql_query = partial(sql_query, LocalTestDb)


class MysqlSpecs(SpecSet):
    people = sql_query("select * from people")
