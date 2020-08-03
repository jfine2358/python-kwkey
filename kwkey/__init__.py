'''PEP 472 -- Support for indexing with keyword arguments

This package provides experimental support for indexing with keyword argments, as proposed in
    https://www.python.org/dev/peps/pep-0472/

We can write
    fn(1, 2, a=3, b=4)
and some users wish to be able to write
    d[1, 2, a=3, b=4]
particularly for use in data science and annotations.

The module provide a helper function
    from kwkeys import o
such that
   d[o(1, 2, a=3, b=4)]
works as well as can be reasonably expected, or so the author thinks.

In module kwkey/example_jfine.py there's an implementation of a class
PointMap. It is a subclass of dict which supports namedtuple style
access to keys.

My approach uses a helper class K for implementing these
experiments. Some wish for the syntax of Python to be extended, to
allow keyword arguments in the d[...] syntax.

If the syntax is extended, I believe a helper class such as K would be
a good idea.  Steven D'Aprano believe that K is irrelevant, except for
experimentation.

This package, once refined and production ready, could be used to
allow the the style of the new syntax to be used with current Python,
via
   d[o(1, 2, a=3, b=4)]
instead of
    d[1, 2, a=3, b=4]

For a recent discussion of PEP 472, see
https://mail.python.org/archives/list/python-ideas@python.org/thread/6OGAFDWCXT5QVV23OZWKBY4TXGZBVYZS/#NYXVHO233EUIAND7WC5SRFXYWC74KSLL

'''

# Convert into a base class?
# Provide another initialiser? K.direct(argv, kwargs)?
# Provide a strmap subclass of tuple for kwargs?


from itertools import chain

from .tools import dunder
from .tools import isdunder
from .tools import undunder

from .tools import dict_from_class


class K(tuple):

    def __new__(cls, *argv, **kwargs):

        # argv is sure to be a tuple.
        if type(argv) is not tuple:
            raise SystemError

        sorted_kwargs = sorted(kwargs.items())
        kwargs_map = tuple(tuple(arg) for arg in sorted_kwargs)
        return tuple.__new__(K, (argv, kwargs_map))

    @property
    def argv(self):
        return self[0]

    @property
    def kwargs(self):
        return self[1]

    def __len__(self):
        '''Length is number of arguments'''

        return len(self.argv) + len(self.kwargs)


    def __repr__(self):

        comma_join = ', '.join
        kwarg_format = '{}={}'.format

        repr_args = comma_join(chain(
            (repr(arg) for arg in self.argv),
            (kwarg_format(*arg) for arg in self.kwargs)
        ))

        return 'K({})'.format(repr_args)

# TODO: test.
def o(*argv, **kwargs):
    '''Store arguments as tuple if possible, otherwise a K.

    >>> o()
    ()
    >>> o(1)
    (1,)
    >>> o(1,)
    (1,)

    As d[1, 2] is equivalent to d[(1, 2)], we have:
    >>> o(1, 2)
    (1, 2)
    >>> o((1, 2))
    (1, 2)

    Two expressions, giving the same key.
    >>> o(1, 2) == o((1, 2))  
    True

    >>> o(a=3)
    K(a=3)
    >>> o(a=3, b=4)
    K(a=3, b=4)
    >>> o(1, 2, a=3, b=4)
    K(1, 2, a=3, b=4)

    Two expressions, giving the same key.
    >>> o(1, 2) == o((1, 2))  
    True
    
    '''

    if kwargs:
        return K(*argv, **kwargs)
    else:
        # Here, argv is sure to be a tuple.
        if type(argv) is not tuple:
            raise SystemError
        if len(argv) == 1:
            arg = argv[0]
            if type(arg) is tuple:
                return argv[0]

        return argv             

class S:
    '''
    >>> s[1:2]
    slice(1, 2, None)
    >>> s[1:2:3]
    slice(1, 2, 3)
    >>> s[:]
    slice(None, None, None)
    >>> s[::]
    slice(None, None, None)
    >>> s[1:2, 4:5]
    (slice(1, 2, None), slice(4, 5, None))
    '''
    
    def __getitem__(self, arg):
        return arg

s = S()

def make_adapter(cls):

    d = dict_from_class(cls)
    if set(d.keys()) != {'__doc__', 'getitem', 'setitem'}:
        raise ValueError(d.keys())

    def adapter(fn, role=None):

        if role is None:
            role = undunder(fn.__name__)

        if role not in {'delitem', 'getitem', 'setitem'}:
            raise ValueError(role)

        if role in {'delitem', 'getitem'}:
            wrapped = cls.getitem(fn)

        elif role == 'setitem':
            wrapped = cls.setitem(fn)

        else:
            raise SystemError(role)

        wrapped.__name__ = dunder(role)
        return wrapped    

    adapter.__name__ = cls.__name__
    return adapter



