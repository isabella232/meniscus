try:
    import uwsgi
    UWSGI = True
except ImportError:
    uwsgi = None
    UWSGI = False


class NativeProxy(object):
    def __init__(self):
        self.server = uwsgi
        # Default timeout = 15 minutes

    def cache_exists(self, key, cache_name):
        if UWSGI:
            return self.server.cache_exists(key, cache=cache_name)
        else:
            return None

    def cache_get(self, key, cache_name):
        if UWSGI:
            return self.server.cache_get(key, cache=cache_name)
        else:
            return None

    def cache_set(self, key, value, cache_name, cache_expires):
        if UWSGI:
            self.server.cache_set(
                key, value, cache=cache_name, expires=cache_expires)

    def cache_update(self, key, value, cache_name, cache_expires):
        if UWSGI:
            self.server.cache_update(
                key, value, cache=cache_name, expires=cache_expires)

    def cache_del(self, key, cache_name):
        if UWSGI:
            self.server.cache_del(key, cache=cache_name)

    def cache_clear(self, cache_name):
        if UWSGI:
            self.server.cache_clear(cache=cache_name)

    def restart(self):
        if UWSGI:
            self.server.reload()
