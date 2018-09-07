"""
The streams module allows you to develop components that produce data for their
dependents and consume data from their dependencies. Requirements are declared
in the standard way, but the resolution step wires together queues between
components.
"""

import copy
import logging
import signal
import sys
import threading
import time

from six.moves.queue import Queue, Empty

from insights import dr

_poison = object()


class Stream(threading.Thread):
    """
    ``Stream`` is the base class for components that want to emit data to
    dependents or consume data from dependencies.
    """

    deep_copy = True

    def __init__(self, *args):
        super(Stream, self).__init__()
        self.observers = []
        self.queue = Queue()
        self.upstreams = {}
        self.log = logging.getLogger(__name__)

        # wire up our input queue to our dependencies
        for a in args:
            if isinstance(a, Stream):
                self.upstreams[a.__class__] = True
                a.observers.append(self)

        # die when the parent dies
        self.daemon = True

    def emit(self, data):
        """
        Use emit to send data to all dependents. If more than one dependent
        exists, a deepcopy of the emitted data is sent to each one if the
        ``deep_copy`` class attribute is ``True``. Otherwise, the same
        reference to the data is sent to all dependents, and it must be thread
        safe.
        """
        if self.deep_copy and data != _poison:
            for i, o in enumerate(self.observers):
                o.queue.put((self.__class__, data if i == 0 else copy.deepcopy(data)))
        else:
            for o in self.observers:
                o.queue.put((self.__class__, data))

    def update(self, src, data):
        """
        The update function is called any time a ``Stream`` dependency emits
        data.

        Args:
            src (class): the class of the ``Stream`` that emitted the data
            data: whatever the ``src`` emitted
        """
        pass

    @property
    def _keep_going(self):
        return any(self.upstreams.values())

    def go(self):
        """
        The default ``go`` implementation gets data off the queue and passes
        it into ``update``. Override ``go`` if you want to produce data, say
        from an external resource, but not consume it from upstream dependencies.
        """
        while self._keep_going:
            try:
                src, evt = self.queue.get(2)
                if evt == _poison:
                    self.upstreams[src] = False
                    self.queue.task_done()
                    continue
                res = self.update(src, evt)
                self.queue.task_done()
                if res is not None:
                    self.emit(res)
            except Empty:
                pass
            except Exception as ex:
                self.log.exception(ex)
                self.queue.task_done()

    def run(self):
        self.go()
        self.emit(_poison)


class stream(dr.ComponentType):
    """
    ``stream`` is the decorator used to signify that a component is a
    ``Stream``. It should only decorate ``Stream`` subclasses. Otherwise, it's
    a component decorator like any other.
    """
    group = "stream"

    def __call__(self, component):
        if not issubclass(component, Stream):
            raise Exception("@stream only valid on Stream subclasses.")
        return super(stream, self).__call__(component)


def run_streams(graph=dr.COMPONENTS["stream"], broker=None):
    """
    Runs the component graph with an optional broker. If any ``Stream``
    instances are present in the results, start them and wait until they're all
    done.
    """
    def handler(signum, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    broker = dr.run(graph, broker=broker)
    streams = broker.get_by_type(stream).values()

    for s in streams:
        s.start()

    # hang out while anything is alive so we can catch signals
    while any(s.is_alive() for s in streams):
        time.sleep(.5)
