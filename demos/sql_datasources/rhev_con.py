import os
from insights import dr
from insights.core.plugins import datasource
from . import PostgresConnection


@datasource()
class rhev_db_config(dict):
    """
    Parse the default rhev database credential file if it exists. This would
    need to be changed or configured externally to point to a valid location.
    """
    filename = "10-setup-database.conf"

    def __init__(self, broker):
        super(rhev_db_config, self).__init__()
        if self.filename is None or not os.access(self.filename, os.R_OK):
            raise dr.SkipComponent()

        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                self[key.strip()] = value.strip()


@datasource(optional=[rhev_db_config])
class RhevCon(PostgresConnection):
    """
    Provide query facilities against the rhev postgres database. Use the db
    config if it was found and parsed. Otherwise, rely on external config
    applied directly to this class.

    We could change this to a required dependency so these collections only
    happen on hosts where the file exists. If RhevCon can't validate a
    connection during Connection.__init__, it'll raise an exception, and no
    dependent datasources will fire.
    """
    db = "engine"
    user = "postgres"

    key_map = {
        "ENGINE_DB_HOST": "host",
        "ENGINE_DB_PORT": "port",
        "ENGINE_DB_USER": "user",
        "ENGINE_DB_PASSWORD": "passwd",
        "ENGINE_DB_DATABASE": "db",
    }

    def __init__(self, broker):
        config = broker.get(rhev_db_config)
        if config:
            for k, v in config.items():
                if k in self.key_map:
                    setattr(self, self.key_map[k], v)
        super(RhevCon, self).__init__(broker)
