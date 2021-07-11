""" Miscellaneous helpful functions and simple objects
"""


class frozendict(dict):
    """ An immutable and hashable dict

    Dict objects aren't hashable; Python has no builtin alternative:
    https://www.python.org/dev/peps/pep-0416/

    This object implements the proposed "frozendict":
     - With no constraint that the values are hashable, only the keys.
     - The order of the underlying dict's keys is ignored when hashing.
     - Inherits from dict only, and thus not explicitly particpate in any metaclass.
    """

    def __hash__(self) -> int:
        return hash(frozenset(self.keys()))

    def __setitem__(self, *args, **kwargs):
        raise NotImplementedError


def bit_count(i: int) -> int:
    """ Count the set bits in an integer i

    Note: Python 3.10 introduced int.bit_count(); replace when it's released.
    """
    count = 0
    while i != 0:
        count += i & 0x1
        i >>= 1
    return count


def mask(lsb: int, length: int) -> int:
    """ Given a least-significant bit and a length, return the corresponding bit mask.

    Examples:
    >>> mask(0, 1) = 0b001
    >>> mask(0, 2) = 0b011
    >>> mask(1, 2) = 0b110
    """
    return ((1 << length) - 1) << lsb


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4