from kwkey.jfine import K
from kwkey.jfine import key_to_jfine


class Dummy:
    '''
    >>> d = Dummy()
    >>> d[1]
    ((1,), {})
    >>> d[1, 2]
    ((1, 2), {})
    >>> d[K(1, 2)]
    ((1, 2), {})
    >>> d[K(1, 2, a=1, b=2)]
    ((1, 2), {'a': 1, 'b': 2})


    >>> del d[K(1, 2, a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})
    >>> d[K(1, 2, a=3, b=4)] = 'value'
    (('value', 1, 2), {'a': 3, 'b': 4})
    >>> d[K(1, 2, a=3, b=4)]
    ((1, 2), {'a': 3, 'b': 4})



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



if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
