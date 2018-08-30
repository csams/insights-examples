#!/usr/bin/env python3.6
from insights import dr
from insights.core.plugins import make_fail, rule


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


@prerequisite(one, two)
def three(a, b):
    return a + b


@rule(one, two, three)
def report(a, b, c):
    return make_fail("ERROR", a=a, b=b, c=c)


if __name__ == "__main__":
    print(dr.run().instances)
