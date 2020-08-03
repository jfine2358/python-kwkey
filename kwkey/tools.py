'''Useful tools

These are not specific to kwkey, and might be better placed somewhere
else.
'''

def isdunder(name):

    return len(name) >= 5 and (name[:2] == name[-2:] == '__')

def dunder(name):

    if name:
        return '__' + name + '__'
    else:
        raise ValueError(name)

def undunder(name):

    if len(name) >= 5:
        if name[:2] == name[-2:] == '__':
            return name[2:-2]
    else:
        raise ValueError(name)


def dict_from_class(cls):

    exclude = {'__dict__', '__module__', '__weakref__'}
#    include = {'__name__', '__mro__'}

    # Gotcha: Can subtract sets, but not add sets!
    # keys = set(cls.__dict__.keys()) - exclude + include
    # TypeError: unsupported operand type(s) for +: 'set' and 'set'

    keys = set(cls.__dict__.keys()) - exclude
    # keys.update(include)

    return dict((k, getattr(cls, k)) for k in keys)
