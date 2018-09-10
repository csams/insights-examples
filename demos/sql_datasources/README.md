This demo extends the framework with sql queries as datasources.

Base classes providing access to Mysql and Postgres databases are in
\_\_init\_\_.py. Subclass them to create components for particular databases.

A standard helper class for creating query datasources is included. It requires
a Connection component and a context that defaults to HostContext. An idiom to
follow is to make a datasource of the Connection subclass you create for a
database and then use partial from functools to specialize sql\_query to execute
only with that connection.

An example Connection specialization called RhevCon is in rhev\_con.py. An
example spec that uses sql\_query and RhevCon is in rhev\_specs.py. A rule that
uses the spec is in some\_rule.py
