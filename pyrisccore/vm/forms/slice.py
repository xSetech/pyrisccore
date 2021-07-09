""" Similar to Python's slice
"""

from dataclasses import dataclass, field

from pyrisccore import PyrisccoreAssertion
from pyrisccore.misc import mask


@dataclass(
    frozen=False,       # <- __post_init__() will fail if this is True.
    unsafe_hash=True    # <- This object is used as though it's actually read-only.
)
class Slice:
    """ A slice of bits

    Examples:
    >>> Slice(0, 0).mask == 0b001
    >>> Slice(0, 0).get(    0b101) == 0b1
    >>> Slice(0, 2).mask == 0b111
    >>> Slice(0, 2).get(    0b101) == 0b101
    >>> Slice(1, 2).mask == 0b110
    >>> Slice(1, 2).get(    0b101) == 0b100
    """

    start: int  # index of the least-significant bit, aka "lsb"
    stop: int   # index of the most-significant bit, aka "msb"

    length: int = field(init=False, hash=False, compare=False)
    mask: int = field(init=False, hash=False, compare=False)

    def __post_init__(self):

        if self.start < 0 or self.stop < 0:
            raise PyrisccoreAssertion("'start' and 'stop' cannot be negative")

        if self.start > self.stop:
            raise PyrisccoreAssertion("'start' is the least-significant index; it must be less-than or equal to 'stop'")

        self.length = self.stop - self.start + 1
        self.mask = mask(self.start, self.length)

    def get(self, source: int) -> int:
        """ Get the value of the slice of bits in an integer "source"
        """
        return (source & self.mask) >> self.start

    def set(self, value: int, destination: int = 0) -> int:
        """ Set the slice of bits in an integer "destination" to a value and return it
        """
        return (
            destination & (~self.mask & mask(0, destination.bit_length()))  # <- zero the 1-bits in the slice of the dest.
            | value << self.start                                           # <- move the value into the slice of the dest.
        )


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4