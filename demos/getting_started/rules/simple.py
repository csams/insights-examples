#!/usr/bin/env python3.6
from insights import dr


class needs(dr.ComponentType):
    pass


@needs()
def one():
    return 1


@needs()
def two():
    return 2


@needs(one, two)
def report(a, b):
    return a + b


if __name__ == "__main__":
    print(dr.run().instances)
