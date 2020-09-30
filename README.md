# PEP 472 -- Support for indexing with keyword arguments

This package provides experimental support for indexing with keyword
argments. This is proposed in [PEP
637](https://www.python.org/dev/peps/pep-0637/). See also PEP 637's
predecessor, [PEP 472](https://www.python.org/dev/peps/pep-0472/).

We can write
```python
    fn(1, 2, a=3, b=4)
```
and some users wish to be able to write
```python
    d[1, 2, a=3, b=4]
```
particularly for use in data science and annotations.


## Helper function `o`

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

## Items-key duality

This package, from version 0.0.2, also provides items-key
duality. Roughly speaking, duality is writing `key[items]` instead of
`items[key]`. Python already supports something like this:

```python
>>> from operator import itemgetter
>>> itemgetter(3)('abcde')
'd'
```

To provide duality we need a special class `X` such that

```python
X(1, 2, a=3, b=4)[items]
```

is equivalent (for the chosen future semantics of keyword arguments)
to:

```python
items[1, 2, a=3, b=4]
```

In current Python the following three statements are already valid
syntax.

```python
X(1, 2, a=3, b=4)[items] = val
val = X(1, 2, a=3, b=4)[items]
del X(1, 2, a=3, b=4)[items]
```

PEP 637 proposes that we allow keywords inside the square brackets
`[...]`. Using items-key duality, we can move the keywords to outside
the square brackets, into a context where they are allowed.

## Semantics of keyword arguments

For this to work, a suitable class `X` must be provided, that
implements the desired semantics. This package provides three such
classes.

### Class `A` - the current semantics

Here's an example. For more, see file `kwkey/test_duality.py`.
```python
>>> A(1, 2)[log] = 'val'
log: setitem(*((1, 2), 'val'), **{})
```

This means that the following three statements are equivalent.
```python
log[(1, 2)] = 'val'
A((1, 2))[log] = 'val'
log.__setitem__((1, 2), 'val')
```

### Class `B` - the semantics proposed by D'Aprano and van Rossum

```python
>>> B(1, 2, a=3, b=4)[log]
log: getitem(*((1, 2),), **{'a': 3, 'b': 4})
```

The previous setitem call is equivalent to
```python
setitem((1, 2), 'val', a=3, b=4)

When no keywords are present, this give the same semantics as class
`A`.

### Class `C` - the semantics propose by Fine

Here the semantics of keywords depend on a special attribute of
`items`, which we call `keyfn`. (Strictly speaking, it should be an
attribure of `type(items)`.

#### Default

The default is to give the same semantics as class `A`.
```python
>>> C((1, 2))[log] = 'val'
log: setitem(*((1, 2), 'val'), **{})
```

The previous setitem call is equivalent to
```python
setitem((1, 2), 'val')
```

#### None

If the special attribute `keyfn` is `None` we get
```python
>>> C(1, 2, a=1, b=2)[nokey] = 'val'
log: setitem(*('val', 1, 2), **{'a': 3, 'b': 4})
```

The previous setitem call is equivalent to
```python
setitem('val', 1, 2, a=3, b=4)
```

#### User supplied `keyfn`

The class `type(items)` can supply its own `keyfn`, to provide custom
behaviour. Here's an example (see `kwkey/test_duality.py` for
details).

```python
>>> C(1, 2, a=1, b=2)[k_log] = 'val'
log: setitem(*(K(1, 2, a=1, b=2), 'val'), **{})
```

The previous setitem call is equivalent to
```python
setitem(K(1, 2, a=1, b=2), 'val')
```
where `K` is a new class, introduced by package `kwkey`.

## Discussion

For discussion of PEP 472 and PEP 637, visit the [Python
ideas](https://mail.python.org/archives/list/python-ideas@python.org/)
miling list.


To test installation, do
```
$ python3 -m kwkey.test
kwkey TestResults(failed=0, attempted=15)
kwkey.duality TestResults(failed=0, attempted=1)
kwkey.example_jfine TestResults(failed=0, attempted=7)
kwkey.jfine TestResults(failed=0, attempted=0)
kwkey.sdaprano TestResults(failed=0, attempted=0)
kwkey.test TestResults(failed=0, attempted=0)
kwkey.test_duality TestResults(failed=0, attempted=65)
kwkey.test_jfine TestResults(failed=0, attempted=19)
kwkey.test_K TestResults(failed=0, attempted=8)
kwkey.test_sdaprano TestResults(failed=0, attempted=25)
kwkey.tools TestResults(failed=0, attempted=0)
```
and check for no failures. (The number of tests will change over time.)