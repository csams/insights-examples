#!/usr/bin/env python
from demos.etl import run_stages, stage
from reader import CsvReader
from writer import JsonWriter, CsvWriter


@stage()
class Input(CsvReader):
    pattern = "quotes.csv"


@stage(Input)
class JsonOutput(JsonWriter):
    filename = "quotes.json"


@stage(Input)
class CsvOutput(CsvWriter):
    filename = "quotes2.csv"


if __name__ == "__main__":
    run_stages()
