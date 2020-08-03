from . import make_adapter
from . import K


@make_adapter
class key_to_jfine:
    '''Allow Function signature decorator, input key, output

    '''

    # This is also used for delitem.
    def getitem(fn):

        # Signature of data coming in.
        def wrapped(self, key):

            if type(key) is tuple:
                return fn(self, *key)

            if type(key) is not K:
                return fn(self, key)

            # Signature of function to be wrapped.
            return fn(self, *key.argv, **dict(key.kwargs))

        return wrapped

    def setitem(fn):

        # Signature of data coming in.
        def wrapped(self, key, val):

            if type(key) is tuple:
                return fn(self, val, *key)

            if type(key) is not K:
                return fn(self, val, key)

            # Signature of function to be wrapped.
            return fn(self, val, *key.argv, **dict(key.kwargs))

        return wrapped


@make_adapter
class jfine_to_key:

    # This is also used for delitem.
    def getitem(fn):

        # Signature of data coming in.
        def wrapped(self, *argv, **kwargs):

            if kwargs:
                return fn(self, K(*argv, **kwargs))

            if len(argv) == 1:
                return fn(self, argv[0])

            # Signature of function to be wrapped.
            return fn(self, argv)

        return wrapped

    def setitem(fn):

        # Signature of data coming in.
        def wrapped(self, val, *argv, **kwargs):

            if kwargs:
                return fn(self, val, K(*argv, **kwargs))

            if len(argv) == 1:
                return fn(self, val, argv[0])

            # Signature of function to be wrapped.
            return fn(self, val, argv)

        return wrapped
