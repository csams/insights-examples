#!/usr/bin/env python
from insights import run, rule, make_pass
from insights.combiners.hostname import hostname
from insights.combiners.uptime import uptime
from insights.parsers.cpuinfo import CpuInfo
from insights.parsers.date import Date
from insights.parsers.meminfo import MemInfo
from insights.parsers.redhat_release import RedhatRelease
from insights.parsers.uname import Uname

CONTENT = """
Hostname: {{fqdn}}

OS      : {{product}} {{major}}.{{minor}}
Kernel  : {{kernel}}
{%- if up_days %}
Uptime  : {{up_days}} days
{%- endif %}
Load Avg: 1min={{load_avg[0]}} 5min={{load_avg[1]}} 15min={{load_avg[2]}}
Time    : {{date}}

Num CPUS: {{cpus}}
Sockets : {{sockets}}
All Mem : {{mem_total}} kB
Av. Mem : {{mem_avail}} kB
""".strip()


@rule(hostname, RedhatRelease, CpuInfo, MemInfo, Uname, uptime, Date)
def report(hn, rhr, cpu, mem, un, ut, dt):
    return make_pass("SYSTEM_INFO",
                     fqdn=hn.fqdn,
                     product=rhr.product,
                     major=rhr.major,
                     minor=rhr.minor,
                     kernel=un.kernel,
                     up_days=ut.updays,
                     load_avg=ut.loadavg,
                     date=dt.data,
                     cpus=cpu.cpu_count,
                     sockets=cpu.socket_count,
                     mem_total=mem.total / 1024,
                     mem_avail=mem.available / 1024)


if __name__ == "__main__":
    run(report, print_summary=True)
