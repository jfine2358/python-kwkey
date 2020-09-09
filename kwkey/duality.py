'''
>>> 1 + 1
2
'''


def make_name_dict(char):

    return {
        'get': (f'_{char}_get__', '__get__'),
        'set': (f'_{char}_set__', '__set__'),
        'del': (f'_{char}_del__', '__del__'),
    }
