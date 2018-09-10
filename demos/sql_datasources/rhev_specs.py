from functools import partial

from insights.core.spec_factory import SpecSet
from demos.sql_datasources.rhev_con import RhevCon
from demos.sql_datasources import sql_query


rhev_query = partial(sql_query, RhevCon)


class RhevSpecs(SpecSet):
    roles = rhev_query("select * from roles")
