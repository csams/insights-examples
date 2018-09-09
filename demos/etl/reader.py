import csv
import json
from glob import glob
from demos.etl import Stage


class Reader(Stage):
    pattern = None

    def go(self):
        files = glob(self.pattern)
        for i in range(self.instance_num, len(files), self.num_instances):
            with open(files[i]) as f:
                self.ingest(f)

    def ingest(self, f):
        raise NotImplemented()


class CsvReader(Reader):
    fieldnames = None

    def ingest(self, f):
        reader = csv.DictReader(f, fieldnames=self.fieldnames)
        for row in reader:
            self.put(row)


class JsonReader(Reader):
    def ingest(self, f):
        for row in f:
            self.put(json.loads(row))
