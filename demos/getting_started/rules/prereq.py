#!/usr/bin/env python3.6
from insights import dr


class needs(dr.ComponentType):
    pass


class prerequisite(dr.ComponentType):
    def invoke(self, broker):
        results = super(prerequisite, self).invoke(broker)
        if results is None:
            raise dr.SkipComponent()
        return results


@needs()
def one():
    return 1


@needs()
def two():
    return 2


@prerequisite()
def three():
    pass


@needs(one, two, three)
def report(a, b, c):
    return a + b + c


if __name__ == "__main__":
    print(dr.run().instances)
