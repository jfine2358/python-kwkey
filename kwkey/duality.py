'''
>>> 1 + 1
2
'''


def make_name_dict(char):

    return {
        'get': (f'_{char}_getitem__', '__getitem__'),
        'set': (f'_{char}_setitem__', '__setitem__'),
        'del': (f'_{char}_delitem__', '__delitem__'),
    }


def lookup_loop(obj, names):

    sentinel = object()

    for name in names:

        value = getattr(obj, name, sentinel)
        if value is not sentinel:
            return value

    # Redo without default to raise exception.
    getattr(obj, name)



class DualityBase:

    name_dict = None            # Supplied by subclass.

    def __init__(self, *argv, **kwargs):

        self.argv = argv
        self.kwargs = kwargs


    def look_up_method(self, other, name):

        cls = type(other)
        names = self.name_dict[name]
        method = lookup_loop(cls, names)

        return method


    def __delitem__(self, other):

        # We need to call a method.
        method = self.look_up_method(other, 'del')

        # We need arguments for the method.
        argv, kwargs = self.make_del_get_args(self.argv, self.kwargs)

        # Call the method, with other as self.
        return method(other, *argv, **kwargs)


    def __getitem__(self, other):

        # We need to call a method.
        method = self.look_up_method(other, 'get')

        # We need arguments for the method.
        argv, kwargs = self.make_del_get_args(self.argv, self.kwargs)

        # Call the method, with other as self.
        return method(other, *argv, **kwargs)


    def __setitem__(self, other, val):

        # We need to call a method.
        method = self.look_up_method(other, 'set')

        # We need arguments for the method.
        argv, kwargs = self.make_set_args(val, self.argv, self.kwargs)

        # Call the method, with other as self.
        return method(other, *argv, **kwargs)


def present_keyfn(argv, kwargs):

    # Check for bad input.
    if type(argv) is not tuple:
        raise ValueError

    if type(kwargs) is not dict:
        raise ValueError

    if kwargs:
        raise ValueError

    if len(argv) == 0:
        raise ValueError

    if len(argv) == 1:
        # If a single arg in argv, it's the key.
        key = argv[0]
    else:
        # Otherwise it's the whole of argv.
        key = argv

    return key


class A(DualityBase):
    '''The present semantics.
    '''

    # Lookup table for item methods. The keys are 'get', 'set', and
    # 'del'. For each key, the corresponding value is the names to
    # lookup, as a tuple.
    name_dict = {
        'get': ('__getitem__',),
        'set': ('__setitem__',),
        'del': ('__delitem__',),
    }

    @staticmethod
    def make_del_get_args(argv, kwargs):

        key = present_keyfn(argv, kwargs)
        return (key,), {}

    @staticmethod
    def make_set_args(val, argv, kwargs):

        key = present_keyfn(argv, kwargs)
        return (key, val), {}


class B(DualityBase):
    '''The D'Aprano and van Rossum semantics.
    '''

    # For 'get' try first '_B_getitem__', then '__getitem__'. And
    # similarly for 'get' and 'set'.
    name_dict = make_name_dict('B')


    @staticmethod
    def make_del_get_args(argv, kwargs):

        if type(argv) is not tuple:
            raise ValueError

        if type(kwargs) is not dict:
            raise ValueError

        if len(argv) == 0:
            key = ()
        else:
            key = present_keyfn(argv, {})

        return (key,), kwargs

    @staticmethod
    def make_set_args(val, argv, kwargs):

        key, kwargs = make_del_get_args(argv, kwargs)
        return (key, val), kwargs
