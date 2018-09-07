#!/usr/bin/env python
from __future__ import print_function
import random
import time

from demos.streaming import run_streams, stream, Stream


class BaseFeed(Stream):
    def __init__(self):
        self.counter = 0
        super(BaseFeed, self).__init__()

    def go(self):
        for _ in range(5):
            time.sleep(random.random() * 2)
            self.emit(self.counter)
            self.counter += 1


@stream()
class FeedOne(BaseFeed):
    pass


@stream()
class FeedTwo(BaseFeed):
    pass


@stream(FeedOne)
class FeedOneModel(Stream):
    def update(self, src, evt):
        return evt * 2


@stream(FeedTwo)
class FeedTwoModel(Stream):
    def update(self, src, evt):
        return evt * 3


@stream(FeedOneModel, FeedTwoModel)
class Watcher(Stream):
    def update(self, src, data):
        print("{src}: {data}".format(src=src, data=data))


if __name__ == "__main__":
    run_streams()
