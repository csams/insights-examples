import logging
import operator
import requests
from cachetools import cachedmethod, TTLCache
from insights import dr


log = logging.getLogger(__name__)


class RemoteResource(object):
    url = None
    timeout = 3

    def fetch(self, url=None):
        return requests.get(url or self.url, timeout=self.timeout).text

    @property
    def data(self):
        return self.fetch()


class CachedRemoteResource(RemoteResource):
    maxsize = 3
    ttl = 15 * 60
    _CACHE = None

    def __init__(self):
        cls = self.__class__
        if not cls._CACHE:
            cls._CACHE = TTLCache(self.maxsize, self.ttl)

    @cachedmethod(operator.attrgetter("_CACHE"))
    def fetch(self, *args, **kwargs):
        return super(CachedRemoteResource, self).fetch(*args, **kwargs)


class remotesource(dr.ComponentType):
    def __call__(self, comp):
        if not issubclass(comp, RemoteResource):
            msg = "remotesource only valid on RemoteResource subclasses."
            raise Exception(msg)
        return super(remotesource, self).__call__(comp)
