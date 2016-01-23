"""
Chapter 2 : Recursion

@author: Alvin Wan
@site: alvinwan.com
"""

def stairs(n):
    """Give the number of ways to take n steps, given that at each step, you
    can choose to take 1, 2, or 3 steps.

    >>> stairs(3)
    4
    >>> stairs(5)
    13
    >>> stairs(10)
    274
    """
    if n <= 2:
        return n
    if n == 3:
        return 4
    return stairs(n-1) + stairs(n-2) + stairs(n-3)


def kstairs(n, k):
    """Give the number of ways to take n steps, given that at each step, you
    can choose to take 1, 2, ... k-2, k-1 or k steps.

    >>> kstairs(5, 2)
    8
    >>> kstairs(5, 5)
    16
    >>> kstairs(10, 5)
    464
    """
    if n == 0:
        return 0
    if n <= k:
        return 2**(n-1)
    return sum([kstairs(n - i, k) for i in range(1, k + 1)])


def det(A):
    """Computes the determinant of a square matrix A using co-factor
    expansion. Assumes A is an nxn but does not assume a specific n.

    >>> A = [
    ... [4, 3, 2, 1],
    ... [0, 2, 1, 4],
    ... [0, 0, 4, 3],
    ... [0, 0, 0, 2]]
    >>> det(A)
    64
    """
    if not A:
        return 1
    subA = lambda i: [row[:i] + row[i+1:] for row in A[1:]]
    is_neg = lambda i: pow(-1, i % 2)  # makes even pos, but odd neg
    return sum(v * is_neg(i) * det(subA(i)) for i, v in enumerate(A[0]))


def permutations(lst):
    """Lists all permutations of the given list.

    >>> permutations(['angie', 'cat'])
    [['angie', 'cat'], ['cat', 'angie']]
    >>> permutations([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    if len(lst) <= 1:
        return [lst]
    total = []
    for i, k in enumerate(lst):
        total.extend([[k] + p for p in permutations(lst[:i] + lst[i+1:])])
    return total


# Problem Variant
# ---------------
# Find all subsets instead of permutations of a list.
# provided by Dibya Jyoti Ghosh
def all_subsets(lst):
    """
    Iteratively finds all possible subsets of a list
    (including the trivial and null subsets)

    >>> all_subsets([1,2,3])
    [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    """
    results = [[]]
    while lst:
        results += [q + [lst[0]] for q in results]
        lst.pop(0)
    return sorted(results,key=len) # To appear in a visually appealing order


def min_pie(pie):
    """Given a tuple of numbers, where each number represents the size of a
    slice of pie, distribute the slices among 2 people as evenly as possible.
    (i.e., minimizing the difference between the sums of two sets of values)

    >>> min_pie((1, 1, 1, 1))
    [((1, 1), (1, 1))]
    >>> min_pie((1, 1, 1, 1, 2, 3))
    [((2, 1, 1), (3, 1, 1)), ((2, 1, 1, 1), (3, 1))]
    >>> min_pie((1, 2, 3, 4, 5, 6))
    [((5, 3, 2), (6, 4, 1)), ((5, 4, 2), (6, 3, 1)), ((5, 3, 2, 1), (6, 4)), ((5, 4, 1), (6, 3, 2))]
    """
    def partition(s):
        if len(s) == 2:
            return [((s[0],), (s[1],))]
        ps = partition(s[1:])
        return [(p1 + (s[0],), p2) for p1, p2 in ps] + \
                [(p1, p2 + (s[0],)) for p1, p2 in ps]
    data = {}
    for p1, p2 in partition(pie):
        data.setdefault(abs(sum(p1) - sum(p2)), {}).setdefault(p1, p2)
    return list(data[min(data)].items())
