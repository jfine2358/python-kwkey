'''
>>> from kwkey import o

>>> pntmap = PointMap()
>>> pntmap[o(1, y=2)] = 'one two'


>>> pntmap
PointMap({Point(x=1, y=2): 'one two'})

>>> pntmap[o(1, y=2)]
'one two'

>>> pntmap[o(y=2)]
((Point(x=1, y=2), 'one two'),)

>>> pntmap[o(y=3)]
()
'''


from collections import namedtuple
from .jfine import key_to_jfine

Point = namedtuple('Point', ('x', 'y'))


class PointMap(dict):

    @key_to_jfine
    def __setitem__(self, val, x, y):

        pnt = Point(x, y)
        dict.__setitem__(self, pnt, val)

    @key_to_jfine
    def __getitem__(self, *argv, **kwargs):

        # Determine the signature.
        ln_v, ln_kw = len(argv), len(kwargs)
        ln_args = ln_v + ln_kw

        # Check the signature.
        if not (1 <= ln_args <= 2):
            raise ValueError

        # Two arguments, so return a single item.
        if ln_args == 2:
            pnt = Point(*argv, **kwargs)
            return dict.__getitem__(self, pnt)

        # One argument, a keyword, so return tuple of items.
        if ln_kw == 1:

            # Expect axis in {'x', 'y'}.
            axis, coord = next(iter(kwargs.items()))

            # Build and return slice of dict.
            return tuple(
                kv_pair for kv_pair in self.items()
                if getattr(kv_pair[0], axis) == coord
            )

        # This cannot happen
        raise SystemError


    def __repr__(self):

        return 'PointMap({})'.format(dict.__repr__(self))
