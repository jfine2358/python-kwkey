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


def getattr_loop(obj, names):

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


    def get_method(self, other, name):

        cls = type(other)
        names = self.name_dict[name]
        method = getattr_loop(cls, names)

        return method

    def __getitem__(self, other):

        # We need to call a method.
        method = self.get_method(other, 'get')

        # We need arguments for the method.
        argv, kwargs = self.call_get(self.argv, self.kwargs)

        # Call the method, with other as self.
        return method(other, *argv, **kwargs)


    def __setitem__(self, other, val):

        # We need to call a method.
        method = self.get_method(other, 'set')

        # We need arguments for the method.
        argv, kwargs = self.call_set(val, self.argv, self.kwargs)

        # Call the method, with other as self.
        return method(other, *argv, **kwargs)


class A(DualityBase):
    '''The present semantics.

    '''

    name_dict = make_name_dict('A')


    # TODO: Move arg checking to init.
    # TODO: Perhaps check via __keyfn__.
    @staticmethod
    def call_get(argv, kwargs):
        if kwargs:
            raise ValueError

        argv = tuple(argv)

        if len(argv) == 1:
            return (argv[0],), {}
        else:
            return (argv,), {}


    @staticmethod
    def call_set(val, argv, kwargs):
        if kwargs:
            raise ValueError

        argv = tuple(argv)
        if len(argv) == 1:
            return (argv[0], val), {}
        else:
            return (argv, val), {}
