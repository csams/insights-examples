#!/usr/bin/env python
from insights import rule, run
from . import remotesource, CachedRemoteResource


@remotesource()
class Google(CachedRemoteResource):
    url = "http://www.google.com"


@rule(Google)
def report(goog):
    print(goog.data)


if __name__ == "__main__":
    run(report, print_summary=True)
