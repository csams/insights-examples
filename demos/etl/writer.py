import json
import csv

from demos.etl import Stage, StopProcessing


class Writer(Stage):
    filename = None

    def go(self):
        if not self.filename:
            raise Exception("Must specify an output file name.")

        if self.num_instances > 1:
            self.filename = self.filename + "." + str(self.instance_num)

        with open(self.filename, "a") as f:
            while True:
                try:
                    src, data = self.get()
                except StopProcessing:
                    break
                else:
                    self.write(data, f)

    def write(self, data, f):
        raise NotImplemented()


class JsonWriter(Writer):
    def write(self, data, f):
        json.dump(data, f)
        f.write("\n")


class CsvWriter(Writer):
    fieldnames = None
    writer = None

    def write(self, data, f):
        if not self.writer:
            fieldnames = self.fieldnames or sorted(data.keys())
            self.writer = csv.DictWriter(f, fieldnames=fieldnames)
            self.writer.writeheader()
        self.writer.writerow(data)
