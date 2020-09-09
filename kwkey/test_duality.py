'''>>> name_dict = make_name_dict('A')

>>> name_dict['get']
('_A_getitem__', '__getitem__')

>>> name_dict['set']
('_A_setitem__', '__setitem__')

>>> name_dict['del']
('_A_delitem__', '__delitem__')



Test data for getattr_loop.
>>> class X: pass
>>> x = X(); x.aaa = 1; x.bbb = 2

Always, return first attribute found, else raise AttributeError.

>>> getattr_loop(x, ('aaa',))
1
>>> getattr_loop(x, ('bbb',))
2
>>> getattr_loop(x, ('ccc',))
Traceback (most recent call last):
AttributeError: 'X' object has no attribute 'ccc'

>>> getattr_loop(x, ('aaa', 'bbb'))
1

>>> getattr_loop(x, ('bbb', 'aaa'))
2

>>> getattr_loop(x, ('aaa', 'ccc'))
1

>>> getattr_loop(x, ('ccc', 'aaa'))
1


>>> a = A(2)
>>> a['abcdef']
'c'

>>> A(2)['abcdef']
'c'

>>> A(slice(2, 5))['abcdef']
'cde'

>>> d = dict()
>>> A('abc')[d] = 5

>>> A('abc')[d]
5

>>> d
{'abc': 5}



'''

from .duality import make_name_dict
from .duality import getattr_loop
from .duality import A
