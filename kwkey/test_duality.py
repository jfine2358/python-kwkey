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


Some odds and ends.
>>> A(slice(2, 5))['abcdef']
'cde'

>>> d = dict()
>>> A('abc')[d] = 5

>>> A('abc')[d]
5

>>> d
{'abc': 5}

Class B give the D'Aprano and van Rossum semantics.

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

'''

from .duality import make_name_dict
from .duality import lookup_loop
from .duality import A
from .duality import B


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
