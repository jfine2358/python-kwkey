'''Test the key_to_sdaprano decorator

The class Dummy_sdaprano shows what is passed to the delitem, getitem
and setitem methods.

The class Dummy_sdaprano_roundtrip provides a round-trip test for the
decorator.

'''
from . import o
from .sdaprano import sdaprano_to_key
from .sdaprano import key_to_sdaprano


class Dummy_sdaprano:
    '''Create a dummy, to see arguments passed.
    >>> d = Dummy_sdaprano()

    # Usual behaviour.
    >>> d[1]
    (1, {})
    >>> d[o(1)]
    (1, {})

    >>> d[1] = 'val'
    (1, 'val', {})
    >>> d[o(1)] = 'val'
    (1, 'val', {})

    # Usual behaviour.
    >>> d[1, 2]
    ((1, 2), {})
    >>> d[o(1, 2)]
    ((1, 2), {})

    >>> d[1, 2] = 'val'
    ((1, 2), 'val', {})

    >>> d[o(1, 2)] = 'val'
    ((1, 2), 'val', {})


    # Keyword arguments present.
    >>> d[o(1, 2, a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})

    # As expected, arguments same for delitem and getitem.
    >>> del d[o(1, 2, a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})

    # Arguments passed to setitem.
    >>> d[o(1, 2, a=3, b=4)] = 'val'
    ((1, 2), 'val', {'a': 3, 'b': 4})

    '''

    @key_to_sdaprano
    def __getitem__(self, key, **kwargs):
        print((key, kwargs))

    @key_to_sdaprano
    def __setitem__(self, key, val, **kwargs):
        print((key, val, kwargs))

    @key_to_sdaprano
    def __delitem__(self, key, **kwargs):
        print((key, kwargs))


class Dummy_sdaprano_roundtrip:

    '''Create a roundtrip
    >>> rt = Dummy_sdaprano_roundtrip()

    >>> rt[1]
    (1, {})

    >>> rt[1, 2]
    ((1, 2), {})

    >>> rt[o(1, 2)]
    ((1, 2), {})

    >>> rt['aaa']
    ('aaa', {})

    >>> rt[o(a=3, b=4)]
    ((), {'a': 3, 'b': 4})

    >>> rt[o(1, a=3, b=4)]
    (1, {'a': 3, 'b': 4})

    >>> rt[o(1, 2, a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})

    >>> rt[o(1, 2, a=3, b=4)] = 'val'
    ((1, 2), 'val', {'a': 3, 'b': 4})

    >>> rt[o((1, 2), a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})

    Two expressions, giving the same key.
    >>> o(1, 2) == o((1, 2))  
    True

    Two expressions, giving different keys.
    >>> o(1, 2, a=3) == o((1, 2), a=3)  
    False

    In Fine's implementation of the D'Aprano API, these two
    expressions are not distinguished.
    >>> rt[o(1, 2, a=3)] == rt[o((1, 2), a=3)]
    ((1, 2), {'a': 3})
    ((1, 2), {'a': 3})
    True

    '''

    @key_to_sdaprano
    @sdaprano_to_key
    def __getitem__(self, key, **kwargs):
        print((key, kwargs))

    @key_to_sdaprano
    @sdaprano_to_key
    def __setitem__(self, key, val, **kwargs):
        print((key, val, kwargs))

    @key_to_sdaprano
    @sdaprano_to_key
    def __delitem__(self, key, **kwargs):
        print((argv, kwargs))
