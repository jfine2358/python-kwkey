'''

>>> name_dict = make_name_dict('A')

>>> name_dict['get']
('_A_get__', '__get__')

>>> name_dict['set']
('_A_set__', '__set__')

>>> name_dict['del']
('_A_del__', '__del__')

'''

from .duality import make_name_dict
