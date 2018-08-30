# insights-examples
Examples of different ways to use insights-core.

`insights-core` supports python 2.6 through 3.3+, and the code in this repo
targets python 3.6.

## Installation
I include insights core as a submodule so its easy to update and play with local
changes.
```
┌[alonzo] tmp/
└> git clone git@github.com:csams/insights-examples.git
Cloning into 'insights-examples'...
remote: Counting objects: 23, done.
remote: Compressing objects: 100% (17/17), done.
remote: Total 23 (delta 6), reused 19 (delta 5), pack-reused 0
Receiving objects: 100% (23/23), 7.83 KiB | 7.83 MiB/s, done.
Resolving deltas: 100% (6/6), done.

┌[alonzo] tmp/
└> cd insights-examples/

┌[alonzo] insights-examples/ (master=)
└> python3.6 -m venv .

┌[alonzo] insights-examples/ (master=)
└> . bin/activate

┌[alonzo] (insights-examples) insights-examples/ (master=)
└> git submodule init insights-core/
Submodule 'insights-core' (https://github.com/RedHatInsights/insights-core.git) registered for path 'insights-core'

┌[alonzo] (insights-examples) insights-examples/ (master=)
└> git submodule update insights-core/
Cloning into '/home/csams/tmp/insights-examples/insights-core'...
Submodule path 'insights-core': checked out 'd60e216a5e74640cf10ab1e4aa23e4ad54e1afb7'

┌[alonzo] (insights-examples) insights-examples/ (master=)
└> pip install -e insights-core -e.
...
┌[alonzo] (insights-examples) insights-examples/ (master=)
└> cd demos/getting_started

┌[alonzo] (insights-examples) getting_started/ (master=)
└> ./driver.py
---------
Progress:
---------
RRR

-------------
Rules Tested:
-------------
rules.convert_to_rule.report
-------------------------------------
{'a': 1, 'b': 2, 'c': 3, 'type': 'rule', 'error_key': 'ERROR'}

rules.rule_with_content.report
---------------------------------------
A: 1
B: 2
C: 3

rules.seed_the_broker.report
-------------------------------------
A: 1
B: 2
C: 3


*******************************
**** Counts By Return Type ****
*******************************
Total Skipped Due To Rule Dependencies Not Met - 0
Total Return Type 'make_pass' - 0
Total Return Type 'make_fail/make_response' - 3
Total Return Type 'make_metadata' - 0
Total Return Type 'make_metadata_key' - 0
Total Exceptions Reported to Broker - 0
```
