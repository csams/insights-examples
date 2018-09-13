#!/usr/bin/env python3.6
"""
Convert one element of the previous examples to a built in `rule` type.
"""
from insights import dr
from insights.core.plugins import make_fail, rule


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


# Rules should return one of None, make_pass, or make_fail. Some rules return
# make_response, but that's just an alias for make_fail.

# The first parameter to make_* should be a string unique to the module, and
# the keyword args can be whatever you like so long as they're json
# serializable. These values are made available to content templates like human
# readable text or ansible plays.
@rule(one, two, three)
def report(a, b, c):
    return make_fail("ERROR", a=a, b=b, c=c)


if __name__ == "__main__":
    print(dr.run().instances)
