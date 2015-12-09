"""
Chapter 5 : Implicit Sequences

@author: Alvin Wan
@site: alvinwan.com
"""

#############
# UTILITIES #
#############

def naturals(start=1):
    n = start
    while True:
        yield n
        n += 1

############################
# ITERATORS AND GENERATORS #
############################

class EveryOtherIter:
    """Iterable that iterates over every other of another sequence (iterator
    or generator).

    >>> for x in EveryOtherIter(naturals()):
    ...   if x > 5:
    ...     break
    ...   print(x)
    ...
    2
    4
    """
    def __init__(self, seq):
        self.seq = seq

    def __next__(self):
        next(self.seq)
        return next(self.seq)

    def __iter__(self):
        return self

def alt_sequences(seq1, seq2, seq3, order):
    """Takes three generators or iterators and a list indicating the order with
    which the sequences are interpolated. If order is [1, 3, 2], seq1 is the
    naturals, seq2 is the naturals starting from 2, and seq3 is the naturals
    starting from 3, the first three elements of the alt_sequences generator
    would be 1, 3, 2.

    >>> gen = alt_sequences(naturals(), naturals(2), naturals(3), [0, 2, 1])
    >>> next(gen), next(gen), next(gen)
    (1, 3, 2)
    """
    tors = [seq1, seq2, seq3]
    while True:
        for i in order:
            yield next(tors[i-1])


def combine(seq0, seq1, f):
    """Takes two generators or iterators and a combiner function f. The ith
    term of combiner function is the ith terms of both seq0 and seq1 combined by
    function f. The length of combiner should be the *longer* of the two
    sequences. The shorter sequence is padded with 0s.

    >>> gen = combine(iter([0, 1]), iter([0, 1, 2, 3]), lambda x, y: x+y)
    >>> for i in gen:
    ...   print(i)
    ...
    0
    2
    2
    3
    """
    def trynext(seq):
        try:
            return next(seq)
        except StopIteration:
            return None
    while True:
        n1, n2 = trynext(seq0), trynext(seq1)
        if n1 is None and n2 is None:
            raise StopIteration
        yield f(n1 or 0, n2 or 0)


def kdeepgen(k, lst):
    """Returns a generator that has k 'depth' and yields all elements of the
    provided lst. 'Depth' is defined as another nested for loop. We define
    the regular generator function to have depth 1.

    >>> for i in kdeepgen(1, [1, 2, 3]):
    ...   print(i)
    ...
    1
    2
    3
    >>> for i in kdeepgen(3, [1, 2, 3]):
    ...   for j in i:
    ...     for k in j:
    ...       print(k)
    ...
    1
    2
    3
    """
    if k == 1:
        for i in lst:
            yield i
        raise StopIteration
    yield kdeepgen(k-1, lst)


import types

def flattengen(gen):
    """Flattens a generator with 'depth', returning a generator with depth 1.

    >>> for i in flattengen(kdeepgen(3, [1, 2, 3])):
    ...   print(i)
    ...
    1
    2
    3
    """
    gens = [gen]
    while gens:
        gen = gens.pop(0)
        if isinstance(gen, types.GeneratorType):
            gens.extend(gen)
        else:
            yield gen
