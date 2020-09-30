'''>>> name_dict = make_name_dict('A')

>>> name_dict['get']
('_A_getitem__', '__getitem__')

>>> name_dict['set']
('_A_setitem__', '__setitem__')

>>> name_dict['del']
('_A_delitem__', '__delitem__')



Test data for lookup_loop.
>>> class X: pass
>>> x = X(); x.aaa = 1; x.bbb = 2

Always, return first attribute found, else raise AttributeError.

>>> lookup_loop(x, ('aaa',))
1
>>> lookup_loop(x, ('bbb',))
2
>>> lookup_loop(x, ('ccc',))
Traceback (most recent call last):
AttributeError: 'X' object has no attribute 'ccc'

>>> lookup_loop(x, ('aaa', 'bbb'))
1

>>> lookup_loop(x, ('bbb', 'aaa'))
2

>>> lookup_loop(x, ('aaa', 'ccc'))
1

>>> lookup_loop(x, ('ccc', 'aaa'))
1


A logging object for use in the doctests below.
>>> log = Log()

The usual way of calling getitem.
>>> log[2]
log: getitem(*(2,), **{})

The dual way of calling getitem, via class A.
>>> A(2)[log]
log: getitem(*(2,), **{})

Retrieving an item, via A.
>>> A(2)['abcdef']
'c'

>>> log[()]
log: getitem(*((),), **{})

The usual way of calling setitem.
>>> log['key'] = 'val'
log: setitem(*('key', 'val'), **{})

The dual way of calling setitem.
>>> A('key')[log] = 'val'
log: setitem(*('key', 'val'), **{})

The usual way of calling delitem.
>>> del log['key']
log: delitem(*('key',), **{})

The dual way of calling delitem.
>>> del A('key')[log]
log: delitem(*('key',), **{})


The next 4 lines all give the same call to getitem.
>>> log[1, 2]
log: getitem(*((1, 2),), **{})

>>> log[(1, 2)]
log: getitem(*((1, 2),), **{})

>>> A(1, 2)[log]
log: getitem(*((1, 2),), **{})

>>> A((1, 2))[log]
log: getitem(*((1, 2),), **{})

>>> A((1, 2))[log] = 'val'
log: setitem(*((1, 2), 'val'), **{})


Some odds and ends.
>>> A(slice(2, 5))['abcdef']
'cde'

>>> d = dict()
>>> A('abc')[d] = 5

>>> A('abc')[d]
5

>>> d
{'abc': 5}

The D'Aprano and van Rossum semantics
=====================================

Class B gives the D'Aprano and van Rossum semantics.

The next two give the SAME result.
>>> B()[log]
log: getitem(*((),), **{})

>>> B(())[log]
log: getitem(*((),), **{})

The next two give DIFFERENT results.
>>> B(1)[log]
log: getitem(*(1,), **{})

>>> B((1,))[log]
log: getitem(*((1,),), **{})

The next two give the SAME result.

>>> B(1, 2)[log]
log: getitem(*((1, 2),), **{})

>>> B((1, 2))[log]
log: getitem(*((1, 2),), **{})

The next two give the SAME result.
>>> B(1, 2, a=3, b=4)[log]
log: getitem(*((1, 2),), **{'a': 3, 'b': 4})

>>> B((1, 2), a=3, b=4)[log]
log: getitem(*((1, 2),), **{'a': 3, 'b': 4})


The Fine semantics
==================

Class C gives the Fine semantics. The behaviour depends on the value
of getattr(type(obj), '__keyfn__', True).

If the value is True, we get the current dict semantics.
>>> getattr(type(log), '__keyfn__', True)
True

>>> C()[log]
Traceback (most recent call last):
ValueError

>>> C(1)[log]
log: getitem(*(1,), **{})

The next two give the SAME result.
>>> C(1, 2)[log]
log: getitem(*((1, 2),), **{})

>>> C((1, 2))[log]
log: getitem(*((1, 2),), **{})

>>> C((1, 2))[log] = 'val'
log: setitem(*((1, 2), 'val'), **{})

If the value is None, we get function call semantics.
>>> class NoKeyfn(Log):
...    __keyfn__ = None

>>> nokey = NoKeyfn()
>>> getattr(type(nokey), '__keyfn__', True) is None
True


>>> C()[nokey]
log: getitem(*(), **{})

>>> C(1)[nokey]
log: getitem(*(1,), **{})

The next two give the DIFFERENT results.
>>> C(1, 2)[nokey]
log: getitem(*(1, 2), **{})

The previous getitem call is equivalent to
#    getitem(1, 2)

>>> C((1, 2))[nokey]
log: getitem(*((1, 2),), **{})

The previous getitem call is equivalent to
#    getitem((1, 2))

>>> C(1, 2, a=3, b=4)[nokey]
log: getitem(*(1, 2), **{'a': 3, 'b': 4})

The previous getitem call is equivalent to
#    getitem(1, 2, a=3, b=4)

For setitem, the value to be assigned comes FIRST.
>>> C(1, 2, a=3, b=4)[nokey] = 'val'
log: setitem(*('val', 1, 2), **{'a': 3, 'b': 4})

The previous setitem call is equivalent to
#    setitem('val' 1, 2, a=3, b=4)

Here the corner case of no arguments.
>>> C()[nokey] = 'val'
log: setitem(*('val',), **{})


We can supply our own keyfn. Here we use the K class, introduced in
v0.0.1 of this package.

>>> class K_Log(Log):
...     @staticmethod
...     def __keyfn__(argv, kwargs):
...         return K(*argv, **kwargs)

>>> k_log = K_Log()

The positional and keyword arguments are recorded in an instance of K.
>>> C()[k_log]
log: getitem(*(K(),), **{})

>>> C(1)[k_log]
log: getitem(*(K(1),), **{})

>>> C(1, 2)[k_log]
log: getitem(*(K(1, 2),), **{})

>>> C((1, 2))[k_log]
log: getitem(*(K((1, 2)),), **{})

>>> C(1, 2, a=1, b=2)[k_log]
log: getitem(*(K(1, 2, a=1, b=2),), **{})

For setitem, the value comes after the 'val' to be assigned.
>>> C(1, 2, a=1, b=2)[k_log] = 'val'
log: setitem(*(K(1, 2, a=1, b=2), 'val'), **{})

The previous setitem call is equivalent to
#   setitem(K(1, 2, a=1, b=2), 'val')

Here the corner case of no arguments.
>>> C()[k_log] = 'val'
log: setitem(*(K(), 'val'), **{})

'''

from .duality import make_name_dict
from .duality import lookup_loop
from .duality import A
from .duality import B
from .duality import C
from . import K


class Log:

    def __init__(self):
        pass

    def __getitem__(self, *argv, **kwargs):
        self._log('getitem', argv, kwargs)

    def __delitem__(self, *argv, **kwargs):
        self._log('delitem', argv, kwargs)

    def __setitem__(self, *argv, **kwargs):
        self._log('setitem', argv, kwargs)

    @staticmethod
    def _log(name, argv, kwargs):
        print(f'log: {name}(*{argv!r}, **{kwargs!r})')
