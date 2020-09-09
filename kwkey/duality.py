'''
>>> 1 + 1
2
'''


def make_name_dict(char):

    return {
        'get': (f'_{char}_get__', '__get__'),
        'set': (f'_{char}_set__', '__set__'),
        'del': (f'_{char}_del__', '__del__'),
    }


def getattr_loop(obj, names):

    sentinel = object()

    for name in names:

        value = getattr(obj, name, sentinel)
        if value is not sentinel:
            return value

    # Redo without default to raise exception.
    getattr(obj, name)
