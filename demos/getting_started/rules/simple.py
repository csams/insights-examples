#!/usr/bin/env python3.6
"""
This module shows how to create a ComponentType and use it. ComponentTypes are
used to express dependencies between components. Core comes with several
specialized types built in, and it's easy to create your own.
"""
from insights import dr


class needs(dr.ComponentType):
    """
    needs is a custom component type. Instances are used to decorate classes or
    functions with their dependencies.
    """
    pass


@needs()
def one():
    """
    Parentheses are required even if there are no arguments. This means `one`
    depends on nothing.
    """
    return 1


@needs()
def two():
    """
    Parentheses are required even if there are no arguments. This means `two`
    depends on nothing.
    """
    return 2


@needs(one, two)
def report(a, b):
    """
    The arguments to the decorator are in the same position as the formal
    parameters of the function. This says "pass the result of `one` as `a` and
    the result of `two` as `b`." More complicated dependency declarations are
    possible, but we don't cover them here.
    """
    return a + b


if __name__ == "__main__":
    print(dr.run().instances)
