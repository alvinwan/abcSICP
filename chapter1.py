"""
Chapter 1 : Higher-Order Function

@author: Alvin Wan
@site: alvinwan.com
"""

def reverse(lst):
    """Without using for, while, or slicing, reverse a list.

    >>> reverse([1, 2, 3, 4, 5, 6])
    [6, 5, 4, 3, 2, 1]
    """

    def other(data):
        i, val = data
        return lst[len(lst) - i - 1]
    return list(map(other, enumerate(lst)))

    # Alternate Solution
    # ------------------
    # It's bad practice to use map for its side effects, because we spend
    # linear space constructing a list of Nones that we're going to dispose of
    # anyways. Regardless, here's a solution that does just that.
    copy = []
    list(map(lambda x: copy.insert(0, x), lst))
    return copy


def first_one(n):
    """Replace each digit in a number with its distance -- in digits -- from the
    first 1 to come *after* it. Any number that does not have a 1 after it will
    be replaced by a 0, and two digits side-by-side have a distance of 1. For
    example, 5312 would become 2100. '5' is 2 away from 1, and '3' is 1 away.
    The '1' itself and '2' have no ones after it, so they both become 0s. Assume
    there is no distance greater than 9.

    >>> first_one(10001)
    43210
    >>> first_one(151646142)
    214321000
    """
    def next_dist(last, dist):
        if last == 1:
            return 1
        return 0 if dist == 0 else dist + 1
    dist, i, new = 0, 0, 0
    while n:
        n, last, new = n // 10, n % 10, new + (10**i * dist)
        dist, i = next_dist(last, dist), i + 1
    return new


def next_look_and_say(n):
    """Returns the next number of the "look-and-say" sequence given the previous
    term n. The first term is 1. To generate a term in the sequence, look at the
    previous term and read it. 1 is "one 1", which translates into 11. 11 is
    then read as "two 1s," which translates into 21.

    >>> next_look_and_say(1)
    11
    >>> next_look_and_say(111221)
    312211
    """
    def count_digits(m):
        m, digit, count = m // 10, m % 10, 1
        while m % 10 == digit:
            m, count = m // 10, count + 1
        return m, digit, count
    new = i = 0
    while n:
        n, digit, count = count_digits(n)
        new, i = new + (10**(i+1) * count) + (10**i * digit), i + 2
    return new

from operator import mul, add, sub, truediv


def crypto_solver(nums, total, ops=[
        (mul, '*'), (add, '+'), (truediv, '/'), (sub, '-')]):
    """Crypto is a puzzle game, where players receive a total and a series of
    numbers. Assume we can only use multiply, divide, add, and subtract, and
    that order of operations doesn't apply ('4+4/2'=4). Write crypto_solver,
    which finds all possible permutations of mathematical operations that will
    yield the total. For example, given [6, 2, 2], total=4, return ['6+2/2']

    >>> soln = crypto_solver([6, 2, 2], 10)  # {'6*2-2', '6+2+2'}
    >>> len(soln)
    2
    >>> '6+2+2' in soln
    True
    >>> '6*2-2' in soln
    True
    """
    rest, solutions = nums[1:], {str(nums[0]): nums[0]}
    for k in rest:
        combos, solutions = solutions, {}
        for streq, subtotal in combos.items():
            for op, strop in ops:
                solutions[streq+strop+str(k)] = op(subtotal, k)
    return {eq for eq, t in solutions.items() if t == total}


def two_largest(lst):
    """Replaces each element of a list with the sum of the two largest numbers
    after it. The last number becomes -1, and the second-to-last will add -1 to
    the last number.

    >>> nums = [51, 31, 1, 43, 23]
    >>> two_largest(nums)
    >>> nums
    [74, 66, 66, 22, -2]
    """
    i, largest, second_largest = len(lst) - 1, -1, -1
    while i >= 0:
        total = largest + second_largest
        if lst[i] > second_largest:
            if lst[i] > largest:
                largest, second_largest = lst[i], largest
            else:
                second_largest = lst[i]
        lst[i] = total
        i -= 1


def matrix_product(A, B):
    """Compute the product of two matrix A and B. If matrix multiplication is
    impossible, raise an error. Recall that the number of columns in the first
    matrix must equal the number of rows in the second matrix.

    >>> I = [
    ... [1, 0, 0, 0],
    ... [0, 1, 0, 0],
    ... [0, 0, 1, 0],
    ... [0, 0, 0, 1]]
    >>> A = [
    ... [4, 3, 2, 1],
    ... [3, 2, 1, 4],
    ... [2, 1, 4, 3],
    ... [1, 4, 3, 2]]
    >>> matrix_product(A, I) == A
    True
    """
    hA, wA, hB, wB = len(A), len(A[0]), len(B), len(B[0])
    assert wA == hB, 'Multiplication impossible: columns of A != rows in B'

    # construct the placeholder matrix
    C = [list(range(wB)) for _ in range(hA)]

    # multiply a specified row in A (y) by a specified column in B (x)
    def multiply(x, y):
        col, row = [row[x] for row in B], A[y]
        C[y][x] = sum(i*j for i, j in zip(col, row))

    # multiply all rows in A by columns in B
    for y in range(hA):
        for x in range(wB):
            multiply(x, y)

    return C
