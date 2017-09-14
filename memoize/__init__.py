from decorator import decorator
import os


# functions that have been decorated
memoize_decorated = set()

def memoize(fun):
    def wrapper(fun, *args, **kwargs):
        if hasattr(fun, '_memoize_keyfunc'):
            key = fun._memoize_keyfunc(*args, **kwargs)
        else:
            key = args, frozenset(iter(kwargs.items()))

        if not key in fun._cache:
            try:
                fun._cache[key] = fun(*args, **kwargs)
            except:
                # Always invalidate cache on exception.
                fun._cache.pop(key, None)
                raise

        return fun._cache[key]

    decorated = decorator(wrapper, fun)
    memoize_zap_cache(decorated)
    memoize_decorated.add(decorated)
    return decorated

def memoize_per_proc(fun):
    """Memoize per process."""
    def keyfunc(*args, **kwargs):
        return os.getpid(), args, frozenset(iter(kwargs.items()))

    return memoize_key(keyfunc)(fun)

def memoize_zap_cache(fun=None):
    """Clear memoized values for all functions (default) or one."""
    if fun is None:
        for fun in memoize_decorated:
            fun.__wrapped__._cache = {}
    else:
        fun.__wrapped__._cache = {}

memoize_cache = {}
def memoize_(fun, *args, **kwargs):
    """An inline memoize."""

    key = fun, args, frozenset(iter(kwargs.items()))

    if not key in memoize_cache:
        try:
            memoize_cache[key] = fun(*args, **kwargs)
        except:
            # Always invalidate cache on exception.
            memoize_cache.pop(key, None)
            raise

    return memoize_cache[key]

def memoizei(meth):
    """A version of memoize that caches data on an *instance* (we
    assume the instance variable is the first passed), thus allowing
    for garbage collection together with the instance."""
    def wrapper(meth, self, *args, **kwargs):
        if hasattr(meth, '_memoize_keyfunc'):
            key = meth, fun._memoize_keyfunc(*args, **kwargs)
        else:
            key = meth, args, frozenset(iter(kwargs.items()))

        if not hasattr(self, '__cache'):
            self.__cache = {}

        if not key in self.__cache:
            # Here, python __-rules help us out for once.
            try:

                self.__cache[key] = meth(self, *args, **kwargs)
            except:
                # Always invalidate cache on exception.
                self.__cache.pop(key, None)
                raise

        return self.__cache[key]

    return decorator(wrapper, meth)

def memoizei_zap_cache(obj):
    """Clear an instance's memoized values."""
    if hasattr(obj, '__cache'):
        delattr(obj, '__cache')

def memoize_key(keyfunc):
    def decorate_function(fun):
        fun._memoize_keyfunc = keyfunc
        return memoize(fun)

    return decorate_function

# We name "singleton" versions of memoize, too, in order to
# distinguish between the usage of memoize as a caching mechanism (as
# in true memoization) and usage where correctness relies on the
# underlying function being called ones (singletons). Right now they
# are equivalent, but it's possible and indeed likely that in the
# future the "memoize" variants will store weakrefs as to allow them
# to be garbage collected aggressively.
singleton, singleton_key, singleton_per_proc, singleton_ = (
    memoize, memoize_key, memoize_per_proc, memoize_
)
