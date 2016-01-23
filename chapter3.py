"""
Chapter 3 : Data Structures

@author: Alvin Wan
@site: alvinwan.com
"""

#############
# UTILITIES #
#############


def print_link(link):
    lst = []
    while link:
        lst.append(link.first)
        link = link.rest
    print(*lst)

class Link:
  """Linked list with a value (first) and a next pointer (rest)"""
  empty = ()
  def __init__(self, first, rest=empty):
    self.first = first
    self.rest = rest

def print_tree(tree):
    level, curr = [], [tree]
    print(tree.entry)
    while curr:
        child = curr.pop(0)
        level.extend(child.branches)
        if not curr:
            if level:
                print(*[t.entry for t in level])
            level, curr = [], level

class Tree:
  """Tree with a value (entry) and a list of subtrees (branches)"""
  def __init__(self, entry, branches=()):
    self.entry = entry
    self.branches = branches

################
# LINKED LISTS #
################


def dot_product(u, v):
    """Compute the dot product of two vectors u and v. If the two linked lists, have different length, raise an error."""
    if u.rest is Link.empty and v.rest is Link.empty:
        return u.first * v.first
    if u.rest is Link.empty or v.rest is Link.empty:
        raise IndexError('Vectors and u and v are not the same length.')
    return u.first * v.first + dot_product(u.rest, v.rest)


def sum_reverse(link):
    """Sets each node's value to be the sum of its value and that of all the
    nodes after it. For example, [1, 2, 3, 4, 5, 6] becomes
    [21, 20, 18, 15, 11, 6]

    >>> lst = Link(1, Link(2, Link(3, Link(4, Link(5, Link(6))))))
    >>> print_link(sum_reverse(lst))
    21 20 18 15 11 6
    """
    if link.rest is Link.empty:
        return
    sum_reverse(link.rest)
    link.first += link.rest.first
    return link


def rotate_left(link, k):
    """Rotate a linked list to the left k times. For example,
    rotate_left([1, 2, 3, 4, 5], 2) would give [3, 4, 5, 1, 2]. Assume that k
    is less than the length of the linked list.

    >>> lst = Link(1, Link(2, Link(3, Link(4, Link(5)))))
    >>> print_link(rotate_left(lst, 2))
    3 4 5 1 2
    """
    pointer = link
    for _ in range(k - 1):
        pointer = pointer.rest
    head, tail, pointer.rest = pointer.rest, pointer.rest, Link.empty
    while tail.rest is not Link.empty:
        tail = tail.rest
    tail.rest = link
    return head


def average(link, k):
    """Conceptually divide the linked list into groups of k until there are no
    more or not enough nodes. Update each node to become the average of the
    group it's in. For k = 3, for example, [1, 2, 3, 4, 5] becomes
    [2, 2, 2, 4.5, 4.5]. Return a new list, and do not modify the original.

    >>> lst = Link(1, Link(2, Link(3, Link(4, Link(5)))))
    >>> print_link(average(lst, 3))
    2.0 2.0 2.0 4.5 4.5
    >>> print_link(lst)
    1 2 3 4 5
    """
    if link is Link.empty:
        return link
    i, pointer, total = 0, link, 0
    while pointer is not Link.empty and i < k:
        i, pointer, total = i + 1, pointer.rest, total + pointer.first
    mean, rest = total / i, average(pointer, k)
    for _ in range(i):
        rest = Link(mean, rest)
    return rest


def is_palindrome(link):
    """Check if a linked list represents a palindrome. Each link in the linked
    list contains one character in the candidate palindrome. Recall that a
    palindrome is any word that is read the same forwards as it is backwards.

    >>> racecar = Link('r', Link('a', Link('c', Link('e', \
        Link('c', Link('a', Link('r')))))))
    >>> is_palindrome(racecar)
    True
    >>> yolo = Link('y', Link('o', Link('l', Link('o'))))
    >>> is_palindrome(yolo)
    False
    """
    def carrier(link, head):
        if link is Link.empty:
            return True, head
        boolean, head = carrier(link.rest, head)
        if boolean and link.first == head.first:
            return True, head.rest
        return False, Link.empty
    return carrier(link, link)[0]


#########
# TREES #
#########


def map_tree(f, t):
    """Maps a function f to every other level of a tree. Apply f to the root,
    and do not modify the original.

    >>> t = Tree(1, [Tree(2, [Tree(4), Tree(5)]), Tree(3, [Tree(6), Tree(7)])])
    >>> print_tree(map_tree(lambda x: x + 3, t))
    4
    2 3
    7 8 9 10
    """
    return Tree(f(t.entry), [Tree(sub.entry, [map_tree(f, subsub)
        for subsub in sub.branches]) for sub in t.branches])


def filter_tree(f, t):
    """Filters a tree, and returns a new tree containing only nodes that pass
    the filter. To simplify the problem, assume that f and t are constructed
    such that the root of the provided tree t always passes the filter f. The
    branches of a deleted node will be pushed up a level.

    >>> t = Tree(1, [Tree(2, [Tree(4, [Tree(5)])]),
    ...     Tree(3, [Tree(6), Tree(7)])])
    >>> print_tree(filter_tree(lambda x: x % 2 == 1, t))
    1
    3 5
    7
    """
    children, branches = [], t.branches[:]
    for b in branches:
        if f(b.entry):
            children.append(filter_tree(f, b))
        else:
            branches.extend(b.branches)
    return Tree(t.entry, children)


def min_leaf(t):
    """Creates a new tree, where each node's value is its distance to the
    closest child leaf.

    >>> t = Tree(1, [Tree(2, [Tree(4), Tree(5)]), Tree(3, [Tree(6)])])
    >>> print_tree(min_leaf(t))
    2
    1 1
    0 0 0
    >>> t = Tree(1, [Tree(2, [Tree(4), Tree(5)]), Tree(3)])
    >>> print_tree(min_leaf(t))
    1
    1 0
    0 0
    """
    if not t.branches:
        return Tree(0)
    branches = [min_leaf(b) for b in t.branches]
    return Tree(min([b.entry for b in branches]) + 1, branches)


def sum_reverse_tree(t):
    """Sets each node's value to be the sum of its value and that of all its
    branches. Modify the original tree, in place.

    >>> t = Tree(1, [Tree(2, [Tree(4), Tree(5)]), Tree(3, [Tree(6)])])
    >>> print_tree(sum_reverse_tree(t))
    21
    11 9
    4 5 6
    """
    t.entry += sum([sum_reverse_tree(b).entry for b in t.branches])
    return t
