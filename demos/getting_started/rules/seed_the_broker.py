#!/usr/bin/env python3.6
"""
This module shows that you can start the computation by using anything you like
as the value for any component. This is useful for testing or integration where
you have the value of a component and don't need or want the component to
compute it for you. Obvious use cases are data ingress.
"""
from insights import dr
from insights.core.plugins import make_fail, rule
from insights.formats.text import HumanReadableFormat as Format


CONTENT = """
A: {{a}}
B: {{b}}
C: {{c}}
""".strip()


class needs(dr.ComponentType):
    pass


class prerequisite(dr.ComponentType):
    def invoke(self, broker):
        result = super(prerequisite, self).invoke(broker)
        if result is None:
            raise dr.SkipComponent()
        return result


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
    broker = dr.Broker()

    # assign the value you want for the component
    broker[one] = 5
    with Format(broker):
        dr.run(broker=broker)
