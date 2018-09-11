# Demos
These are examples of things you can do with the insights-core framework.
They're illustrative ideas that aren't of production quality.

## getting_started
The getting started demo shows the very basics of how to use insights-core as a
library for expressing dependencies between components. It has some simple rules,
rules with content, some formatting, and a driver script that shows how to load
and run plugins programmatically.

## streaming
The streaming project uses insights-core to wire together components that run in
independent threads and communite with queues. Something like it can be used to
monitor queues or other endpoints and feed data from them downstream.

## etl
The etl demo is similar to the streaming demo except you can configure multiple
instances of each component type, instances of each type can consume from the
same queue or a queue per instance, and each instance runs in its own process.
The demo includes simple reader and writer components for csv and json files.

## remote\_datasources
This project shows how we might support components that provide data from http
endpoints. The cached version of the resource class uses a cachetools TTLCache.


## sql\_datasources
Here we show a way to connect to mysql or postgres databases and provide the
results of sql queries to downstream components like parsers and rules. A RHEV
postgres database is required for this demo.
