#!/usr/bin/env python3.6
from insights import dr
from insights.core.plugins import make_fail, rule
from insights.formats.text import HumanReadableFormat as Format

ERROR_KEY = "ERROR"

# this is a jinja2 template
ERROR_CONTENT = """
A: {{a}}
B: {{b}}
C: {{c}}
""".strip()

# the keys here match the first parameter to make_fail and make_pass
CONTENT = {
    ERROR_KEY: ERROR_CONTENT
}


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

    # any json serializable values may be passed as keyword arguments and may
    # be used in the content templates.
    return make_fail(ERROR_KEY, a=a, b=b, c=c)


if __name__ == "__main__":
    broker = dr.Broker()
    with Format(broker):
        dr.run(broker=broker)
