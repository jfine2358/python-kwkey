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


>>> log = Log()

>>> log[2]
log: getitem(*(2,), **{})

>>> A(2)[log]
log: getitem(*(2,), **{})

>>> A(2)['abcdef']
'c'

>>> log[()]
log: getitem(*((),), **{})

>>> log['key'] = 'val'
log: setitem(*('key', 'val'), **{})

>>> A('key')[log] = 'val'
log: setitem(*('key', 'val'), **{})



>>> A(slice(2, 5))['abcdef']
'cde'

>>> d = dict()
>>> A('abc')[d] = 5

>>> A('abc')[d]
5

>>> d
{'abc': 5}


>>> log = Log()

>>> log[1, 2, 'a']
log: getitem(*((1, 2, 'a'),), **{})

'''

from .duality import make_name_dict
from .duality import lookup_loop
from .duality import A





class Log:

    def __init__(self):
        pass

    def __getitem__(self, *argv, **kwargs):
        self._log('getitem', argv, kwargs)

    def __delitem__(self, *argv, **kwargs):
        self._log('delitem', argv, kwargs)
        print(f'del: {key!r}')

    def __setitem__(self, *argv, **kwargs):
        self._log('setitem', argv, kwargs)

    @staticmethod
    def _log(name, argv, kwargs):
        print(f'log: {name}(*{argv!r}, **{kwargs!r})')
