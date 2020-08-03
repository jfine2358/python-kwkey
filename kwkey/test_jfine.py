'''Test the key_to_jfine decorator

The class Dummy_jfine shows what is passed to the delitem, getitem and
setitem methods.

The class Dummy_jfine_roundtrip provides a round-trip test for the
decorator.
'''
from . import o
from .jfine import jfine_to_key
from .jfine import key_to_jfine


class Dummy_jfine:
    '''Create a dummy, to see arguments passed.
    >>> d = Dummy_jfine()

    # Usual behaviour.
    >>> d[1]
    ((1,), {})
    >>> d[o(1)]
    ((1,), {})

    >>> d[1] = 'val'
    (('val', 1), {})
    >>> d[o(1)] = 'val'
    (('val', 1), {})

    # Usual behaviour.
    >>> d[1, 2]
    ((1, 2), {})
    >>> d[o(1, 2)]
    ((1, 2), {})

    >>> d[1, 2] = 'val'
    (('val', 1, 2), {})
    >>> d[o(1, 2)] = 'val'
    (('val', 1, 2), {})


    # Keyword arguments present.
    >>> d[o(1, 2, a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})

    # As expected, arguments same for delitem and getitem.
    >>> del d[o(1, 2, a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})

    # Arguments passed to setitem.
    >>> d[o(1, 2, a=3, b=4)] = 'val'
    (('val', 1, 2), {'a': 3, 'b': 4})

    '''

    @key_to_jfine
    def __getitem__(self, *argv, **kwargs):
        print((argv, kwargs))

    @key_to_jfine
    def __setitem__(self, *argv, **kwargs):
        print((argv, kwargs))

    @key_to_jfine
    def __delitem__(self, *argv, **kwargs):
        print((argv, kwargs))


class Dummy_jfine_roundtrip:

    '''
    Create a roundtrip
    >>> rt = Dummy_jfine_roundtrip()

    >>> rt[1]
    ((1,), {})

    >>> rt[1, 2]
    (((1, 2),), {})

    >>> rt[(0, 1, 2)]
    (((0, 1, 2),), {})

    >>> rt['aaa']
    (('aaa',), {})

    >>> rt[o(1, 2, a=3, b=4)]
    ((K(1, 2, a=3, b=4),), {})

    >>> rt[o(1, 2, a=3, b=4)] = 'val'
    (('val', K(1, 2, a=3, b=4)), {})
    '''

    @key_to_jfine
    @jfine_to_key
    def __getitem__(self, *argv, **kwargs):
        print((argv, kwargs))

    @key_to_jfine
    @jfine_to_key
    def __setitem__(self, *argv, **kwargs):
        print((argv, kwargs))

    @key_to_jfine
    @jfine_to_key
    def __delitem__(self, *argv, **kwargs):
        print((argv, kwargs))
