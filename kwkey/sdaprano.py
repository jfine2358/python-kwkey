'''API proposed by Steven D'Aprano 

Important note: This is Jonathan Fine's understanding of the API
proposed by Steven D'Aprano. However, Steven hasn't seen this code
yet. I hope he regards it as a fair representation of what he proposed
on the Python-ideas mailing list. I'll gladly accept changes.

'''


from . import make_adapter
from . import K

# Steven D'Aprano wrote the following:
# See https://mail.python.org/archives/list/python-ideas@python.org/message/NYXVHO233EUIAND7WC5SRFXYWC74KSLL/

# Existing signatures would stay the same:

#  def __getitem__(self, item)
#  def __setitem__(self, item, value)
# but those who wanted keyword args could add them, with or without 
# defaults:

#  def __getitem__(self, item, *, spam=None)
#  def __setitem__(self, item, value, *, spam, eggs=None)
# I trust the expected behaviour is obvious, but in case it's not:

# myobj[1, 2, spam=3]  # calls __getitem__((1, 2), spam=3)

# myobj[1, 2, spam=3]  = 999
# # calls __setitem__((1, 2), 999, spam=3, eggs=None)
# (And similarly for delitem of course.)


@make_adapter
class key_to_sdaprano:
    '''Allow Function signature decorator, input key, output

    '''

    # This is also used for delitem.
    def getitem(fn):

        # Signature of data coming in.
        def wrapped(self, key):

            # d['a'] gives ('a',) as key, i.e. argv.
            if type(key) is tuple:
                if len(key) == 1:
                    return fn(self, key[0])

            # Type K means we have keywords.
            if type(key) is K:
                return fn(self, key.argv, **dict(key.kwargs))

            # Otherwise, use the key as is.
            return fn(self, key)

        return wrapped

    def setitem(fn):

        # Signature of data coming in.
        def wrapped(self, key, val):
            
            if type(key) is tuple:
                if len(key) == 1:
                    return fn(self, key[0], val)

            if type(key) is K:
                return fn(self, key.argv, val, **dict(key.kwargs))
                
            return fn(self, key, val)

        return wrapped


@make_adapter
class sdaprano_to_key:

    # This is also used for delitem.
    def getitem(fn):

        # Signature of data coming in.
        def wrapped(self, arg, **kwargs):

            if type(arg) is tuple:
                if len(arg) == 1:
                    arg = arg[0]

            return fn(self, arg, **kwargs)

        return wrapped

    def setitem(fn):

        # Signature of data coming in.
        def wrapped(self, arg, val, **kwargs):

            if type(arg) is tuple:
                if len(arg) == 1:
                    arg = arg[0]

            return fn(self, arg, val, **kwargs)

        return wrapped
