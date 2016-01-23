"""
Chapter 4 : Object Oriented Programming

@author: Alvin Wan
@site: alvinwan.com
"""

def hailstone_chicken(i):
    """Return a function hailstone(start) that prints the hailstone sequence for
    a given start. For every ith number n of the hailstone sequence,
    print a string with 'chicken' repeated n times instead of n itself.
    Reminder: If the number is even, divide it by 2. If the number is odd,
    multiply by 3 and add 1.

    >>> hailstone = hailstone_chicken(3)
    >>> hailstone(8)
    8
    4
    chickenchicken
    1
    """
    n = 0
    def hailstone(start):
        nonlocal n
        n += 1
        print(start if n % i else 'chicken' * start)
        if start > 1:
            if start % 2 == 0:
                return hailstone(start // 2)
            return hailstone(3 * start + 1)
    return hailstone


def fib_range(x, y):
    """Return a function that returns the next number in a series of fibonacci
    numbers, starting from x and ending with y, excluding y. Raise a
    StopIteration exception if there are no more numbers in the sequence.

    >>> fib = fib_range(2, 20)
    >>> [fib() for _ in range(5)]
    [2, 3, 5, 8, 13]
    >>> fib()
    Traceback (most recent call last):
        ...
    StopIteration
    """
    prev, curr = 0, 1
    def fib():
        nonlocal prev, curr
        if curr > y:
            raise StopIteration()
        prev, curr = curr, curr + prev
        return fib() if prev < x else prev
    return fib


def create_complex():
    """Without using nonlocal, returns a function complex(a=None, b=None), and
    intializes the complex number to 0. complex(a, b) adds a complex number
    a + bi to the complex number, and complex() returns a stringified form of
    the complex.

    >>> complex = create_complex()
    >>> complex(5, 3)
    >>> complex()
    '5+3i'
    >>> complex(7, 3)
    >>> complex()
    '12+6i'
    """
    n = {'real': 0, 'imag': 0}
    def complex(a=None, b=None):
        if not a:
            return '%d+%di' % (n['real'], n['imag'])
        n['real'] += a
        n['imag'] += b
    return complex


def call_depth():
    """Returns two function f and g. g returns the number of times f was called
    (n) multiplied by the maximum "depth" d of a call expression. For g(), d=1
    and f wasn't called so n=0. That makes d*n=0. For g(f()), d=2, n=1, d*n=2.
    For g(f(f())) d=3 and n=2, d*n=6. For g(f(f(), f(f()))), d=4, n=4, d*n=16.

    >>> f, g = call_depth()
    >>> g(f(f()))
    6
    >>> f, g = call_depth()
    >>> g(f(f(), f(f())))
    16
    """
    n = 0
    def f(*args):
        nonlocal n
        n += 1
        if not args:
            return 1
        return max(args) + 1
    return f, lambda depth: n * (depth + 1)


def fizzbuzzes(rules):
    """Given a dictionary rules mapping integers i => strings s, returns a
    function that prints a sequence with a few modifications: apply all rules
    from the provided dictionary, where each ith term is replaced with s.
    Higher values of i take precedence over lower values of i.

    >>> fizzbuzz = fizzbuzzes({3: 'fizz', 6: 'buzz', 2: 'huehue'})
    >>> fizzbuzz(range(1, 7))
    1
    huehue
    fizz
    huehue
    5
    buzz
    """
    keys = sorted(rules.keys(), reverse=True)
    def fizzbuzz(sequence):
        for n in sequence:
            candidates = [rules[k] for k in keys if n % k == 0]
            print(candidates[0] if candidates else n)
    return fizzbuzz


from copy import deepcopy

maze = '''
+----------+
| | |      |
| | | | ---|
| |   |    |
|   | |  | |
+----------+
'''

maze2 = '''
+----+
|    |
|    |
|    |
|    |
+----+
'''

def maze_solver(maze, start=(1, 1), end=None,
        moves=lambda x, y: ((x+1, y), (x-1, y), (x, y+1), (x, y-1)),
        is_wall=lambda maze, x, y: maze[y][x] != ' '):
    """Solves a maze, given a stringified maze, an optional start
    (default (1, 1)), an optional end (default to the bottom right), and an
    optional function moves that returns all possible moves given an x, y
    (default up, down, right, left). Your solution does not need to be
    optimized, and return the original maze if no path exists.
    +----------+
    | | |      |
    | | | | ---|
    | |   |    |
    |   | |  | |
    +----------+
    Calling maze_solver(maze) should output the following.
    +----------+
    |*| |***   |
    |*| |*|*---|
    |*|***|****|
    |***| |  |*|
    +----------+

    >>> maze_solver(maze)
    +----------+
    |*| |***   |
    |*| |*|*---|
    |*|***|****|
    |***| |  |*|
    +----------+
    >>> maze_solver(maze, end=(5, 4))
    +----------+
    |*| |      |
    |*| | | ---|
    |*|***|    |
    |***|*|  | |
    +----------+
    >>> only_down_right = lambda x, y: ((x+1, y+1),)
    >>> maze_solver(maze2, moves=only_down_right)
    +----+
    |*   |
    | *  |
    |  * |
    |   *|
    +----+
    >>> maze_solver(maze, moves=only_down_right)  # no solution
    +----------+
    | | |      |
    | | | | ---|
    | |   |    |
    |   | |  | |
    +----------+
    """
    maze = list(map(list, maze.strip().splitlines()))
    width, height, visited = len(maze[0]), len(maze), []
    outside = lambda x, y: width < x < 0 or height < y < 0
    def find(place):
        if place in (end, (width-2, height-2)):
            return (place,)
        if is_wall(maze, *place) or place in visited or outside(*place):
            return ()
        visited.append(place)
        for path in filter(bool, map(find, moves(*place))):
            return (place,) + path
    for x, y in find(start) or ():
        maze[y][x] = '*'
    print('\n'.join([''.join(row) for row in maze]))
