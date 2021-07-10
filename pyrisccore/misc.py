""" Miscellaneous helpful functions and simple objects
"""


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