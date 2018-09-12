#!/usr/bin/env python3.6
from insights import dr
from insights.formats.text import HumanReadableFormat as Formatter
# from insights.formats._json import JsonFormat as Formatter


dr.load_components("rules")
broker = dr.Broker()
with Formatter(broker):
    dr.run(broker=broker)
