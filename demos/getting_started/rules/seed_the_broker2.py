#!/usr/bin/env python3.6
"""
This is similar to seed_the_broker.py except we provide data for a few
components built into core.
"""
from insights import dr
from insights.combiners.hostname import hostname
from insights.core.plugins import make_fail, rule
from insights.formats.text import HumanReadableFormat as Format
from insights.parsers.dmesg import DmesgLineList
from insights.specs import Specs
from insights.tests import context_wrap


MSGINFO = """
[    0.000000] tsc: Fast TSC calibration using PIT
[    0.000000] tsc: Detected 2693.827 MHz processor
[    0.000026] Calibrating delay loop (skipped), value calculated using timer frequency.. 5387.65 BogoMIPS (lpj=2693827)
[    0.000028] pid_max: default: 32768 minimum: 301
[    0.000048] Security Framework initialized
[    0.000053] SELinux:  Initializing.
[    0.000059] SELinux:  Starting in permissive mode
[    0.001043] Dentry cache hash table entries: 2097152 (order: 12, 16777216 bytes)
[    0.003709] Inode-cache hash table entries: 1048576 (order: 11, 8388608 bytes)
[    0.004791] Mount-cache hash table entries: 4096
[    0.004944] Initializing cgroup subsys memory
[    0.004958] Initializing cgroup subsys net_prio
[    0.004982] CPU: Physical Processor ID: 0
[    0.004983] CPU: Processor Core ID: 0
[    0.004987] ENERGY_PERF_BIAS: Set to 'normal', was 'performance'
[    0.004987] ENERGY_PERF_BIAS: View and update with x86_energy_perf_policy(8)
[    0.005828] mce: CPU supports 9 MCE banks
[    0.005841] CPU0: Thermal monitoring enabled (TM1)
[    0.005851] Last level iTLB entries: 4KB 0, 2MB 0, 4MB 0
[    0.005852] Last level dTLB entries: 4KB 64, 2MB 0, 4MB 0
[    0.005853] tlb_flushall_shift: 6
[    0.005933] Freeing SMP alternatives: 28k freed
[    0.006814] ACPI: Core revision 20130517
[    0.014594] ACPI: All ACPI Tables successfully acquired
[    0.015670] ftrace: allocating 25815 entries in 101 pages
[    0.024837] smpboot: Max logical packages: 2
[    0.024847] DMAR: Host address width 39
[    0.025063] Enabling x2apic
[    0.025064] Enabled x2apic
[    0.025069] Switched APIC routing to cluster x2apic.
[    0.025482] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.035484] smpboot: CPU0: Intel(R) Core(TM) i7-4800MQ CPU @ 2.70GHz (fam: 06, model: 3c, stepping: 03)
[    0.035490] TSC deadline timer enabled
"""


CONTENT = """
Host: {{hn}}
A: {{a}}
B: {{b}}
C: {{c}}
SELinux lines:
{%- for line in selinux %}
{{line.raw_message}}
{%- endfor %}
""".strip()


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


@rule(one, two, three, hostname, DmesgLineList)
def report(a, b, c, hn, dmsg):
    selinux = dmsg.get("SELinux")
    return make_fail("ERROR", a=a, b=b, c=c, hn=hn.fqdn, selinux=selinux)


if __name__ == "__main__":
    broker = dr.Broker()
    broker[Specs.hostname] = context_wrap("www.example.com")
    broker[Specs.dmesg] = context_wrap(MSGINFO)
    with Format(broker):
        dr.run(broker=broker)
