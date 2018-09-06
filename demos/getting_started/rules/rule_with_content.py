#!/usr/bin/env python3.6
"""
Show a rule with an embedded content template.
"""
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

# the keys here match the first parameter to make_fail and make_pass. Each
# value is a template to render for the given key. Keys traditionally have an
# 'ERROR_' prefix.
CONTENT = {
    ERROR_KEY: ERROR_CONTENT
}


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

    # any json serializable values may be passed as keyword arguments and may
    # be used in the content templates.
    return make_fail(ERROR_KEY, a=a, b=b, c=c)


if __name__ == "__main__":
    broker = dr.Broker()
    # Core has a few formats for rendering rule output: human readable, json,
    # and yaml. The json format is the same as that used by the service
    # wrappers for communicating rule results to other systems.
    with Format(broker):
        dr.run(broker=broker)
