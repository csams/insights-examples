#!/usr/bin/env python3.6
"""
This module shows a ComponentType that customizes execution of the components
it decorates. We create a `prerequisite` type that prevents dependents from
executing if its component returns `None`.
"""
from insights import dr


# This is the same component type from `simple.py`.
class needs(dr.ComponentType):
    pass


class prerequisite(dr.ComponentType):
    """
    If a prerequisite isn't met, nothing that depends on it should execute. We
    use the convention that returning None means the prerequisite isn't met. In
    that case, we raise a special `Exception` that will prevent from firing any
    component that requires the prerequisite. The effect is transitive, so any
    component that requires a component that doesn't execute for any reason
    also will not execute.
    """
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
    pass  # implied return None


# `report` will not attempt to execute since `three` returns `None`.
@needs(one, two, three)
def report(a, b, c):
    return a + b + c


if __name__ == "__main__":
    print(dr.run().instances)
