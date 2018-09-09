import multiprocessing as mp
import signal
import sys
import traceback
from collections import Counter, defaultdict
from itertools import chain

from insights import dr
from six.moves.queue import Empty


class StopProcessing(BaseException):
    """ Sent to dependent processes when a stage is done. """
    pass


class Stage(mp.Process):
    num_instances = 1
    shared_queue = True
    queue = None
    stop_queue = None
    counter = Counter()

    def __init__(self, *args):
        super(Stage, self).__init__()
        self.instance_num = Stage.counter[self.__class__]
        Stage.counter[self.__class__] += 1

        if self.shared_queue and not self.__class__.queue:
            self.__class__.queue = mp.Queue()
        if not self.shared_queue:
            self.queue = mp.Queue()

        self.observers = defaultdict(list)

        # wire up our input queue to our dependencies
        cls = self.__class__
        for a in args:
            if isinstance(a, list) and isinstance(a[0], Stage):
                for i in a:
                    if self.queue not in i.observers[cls]:
                        i.observers[cls].append(self.queue)

        # die when the parent dies
        self.daemon = True

    def put(self, data, target=None):
        if target is None:
            for q in chain.from_iterable(self.observers.values()):
                q.put((self.__class__, data))
        else:
            for q in self.observers[target]:
                q.put((self.__class__, data))

    def get(self):
        while True:
            try:
                data = self.queue.get(2)
                if data is StopProcessing:
                    raise StopProcessing
            except Empty:
                pass
            else:
                return data

    def go(self):
        """
        The default ``go`` implementation gets data off the queue and passes
        it into ``update``. Override ``go`` if you want to produce data but not
        consume it from upstream dependencies.
        """
        while True:
            try:
                data = self.get()
                res = self.update(*data)
                if res is not None:
                    self.put(res)
            except StopProcessing:
                break
            except Exception as ex:
                break
                traceback.print_exc()

    def run(self):
        self.go()
        self.stop_queue.put(self.__class__)

    def update(self, src, data):
        pass


class stage(dr.ComponentType):
    group = "stage"

    def invoke(self, broker):
        create = super(stage, self).invoke
        return [create(broker) for _ in range(self.component.num_instances)]

    def __call__(self, comp):
        if not issubclass(comp, Stage):
            raise Exception("%s must be a subclass of Stage" % dr.get_name(comp))
        return super(stage, self).__call__(comp)


def run_stages(graph=dr.COMPONENTS["stage"], broker=None):
    """
    Runs the component graph with an optional broker. If any ``Stage``
    instances are present in the results, start them and wait until they're all
    done.
    """
    def handler(signum, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    broker = dr.run(graph, broker=broker)
    if broker.exceptions:
        print(broker.tracebacks)
        sys.exit(0)

    stages = broker.get_by_type(stage)
    dependencies = {}
    dependents = {}
    instances = []
    stop_queue = mp.Queue()

    for s, v in stages.items():
        dependencies[s] = set(d for d in graph[s] if issubclass(d, Stage))
        dependents[s] = set(d for d in dr.get_dependents(s) if issubclass(d, Stage))
        for i in v:
            i.stop_queue = stop_queue
            i.start()
            instances.append(i)

    done_counter = Counter()
    finished = set()

    def handle_finished():
        try:
            done = stop_queue.get(0.5)
        except Empty:
            return
        else:
            done_counter[done] += 1
            if done_counter[done] == done.num_instances:
                finished.add(done)
                for d in dependents[done]:
                    if dependencies[d].issubset(finished):
                        for i in stages[d]:
                            i.queue.put(StopProcessing)
                            if not d.shared_queue:
                                i.queue.close()
                                i.queue.join_thread()
                        if d.shared_queue:
                            d.queue.close()
                            d.queue.join_thread()
                        for i in stages[d]:
                            i.join()

    while any(s.is_alive() for s in instances):
        handle_finished()
