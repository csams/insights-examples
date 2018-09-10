#!/usr/bin/env python
from insights import rule, run
from insights.core.plugins import make_fail
from demos.sql_datasources.rhev_specs import RhevSpecs as Specs


CONTENT = """
{%- for r in roles %}
Name: {{r.name}}
Description: {{r.description}}
{% endfor %}
""".strip()


@rule(Specs.roles)
def report(roles):
    return make_fail("ERROR", roles=roles)


if __name__ == "__main__":
    run(report, print_summary=True)
