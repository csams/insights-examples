#!/usr/bin/env python
from insights import rule, run
from insights.core.plugins import make_pass
from demos.sql_datasources.sql_specs import MysqlSpecs as Specs


CONTENT = """
{%- for p in people %}
Name: {{p.name}}
Age: {{p.age}}
{% endfor %}
""".strip()


@rule(Specs.people)
def report(ppl):
    return make_pass("PASSED", people=ppl)


if __name__ == "__main__":
    run(report, print_summary=True)
