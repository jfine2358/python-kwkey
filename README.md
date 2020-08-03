# PEP 472 -- Support for indexing with keyword arguments

This package provides experimental support for indexing with keyword
argments, as proposed in https://www.python.org/dev/peps/pep-0472/

We can write
```python
    fn(1, 2, a=3, b=4)
```
and some users wish to be able to write
```python
    d[1, 2, a=3, b=4]
```
particularly for use in data science and annotations.

The module provide a helper function
```python
    from kwkeys import o
```
such that
```python
   d[o(1, 2, a=3, b=4)]
```
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
```python
   d[o(1, 2, a=3, b=4)]
```
instead of
```python
    d[1, 2, a=3, b=4]
```

For a recent discussion of PEP 472, see
https://mail.python.org/archives/list/python-ideas@python.org/thread/6OGAFDWCXT5QVV23OZWKBY4TXGZBVYZS/#NYXVHO233EUIAND7WC5SRFXYWC74KSLL


To test installation, do
```
$ python3 -m kwkey.test
kwkey.jfine TestResults(failed=0, attempted=0)
kwkey.example_jfine TestResults(failed=0, attempted=7)
kwkey.tools TestResults(failed=0, attempted=0)
kwkey.test TestResults(failed=0, attempted=0)
kwkey.test_K TestResults(failed=0, attempted=8)
kwkey.sdaprano TestResults(failed=0, attempted=0)
```
and check for no failures. (The number of tests will change over time.)