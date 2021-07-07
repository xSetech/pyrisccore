""" A "field" is a slice of a word with distinct value
"""

from dataclasses import dataclass, field
from typing import Optional, Union

from pyrisccore import PyrisccoreAssertion
from pyrisccore.vm.forms.word import WORD, Word


@dataclass(
    frozen=False,       # <- __post_init__() will fail if this is True.
    unsafe_hash=True    # <- Once a Field is instantiated, it's effectively frozen.
)
class Field:
    """ A slice of a "word" with distinct value
    """

    # The range of bits in a word for this field's value.
    source: slice

    # The name of the field; multiple Field instances can share this value
    # to indicate that the bits of their values come from multiple slices.
    name: Optional[str] = None
    source_mask: int = field(init=False)

    # Declare which of the source bits map to specific bits of the value.
    # For example, see the "imm" field of the J-Type instruction format.
    destination: Optional[slice] = None
    destination_mask: Optional[int] = field(init=False, default=None)

    # Declare that the value of this field is linked to the value of another field
    # rather than the instruction word. This is given as either the name of a field
    # in the instruction format or as the index of a field in the instruction format
    # counting from the least significant bit (0-indexing).
    parent: Optional[Union[str, int]] = None

    # Number of bits required to represent this field's value.
    size: int = field(init=False)

    def __post_init__(self):

        # Enforce constraints on the source slice
        self._validate_slice(self.source)
        size_src = self.source.stop - self.source.start + 1

        # Use the source slice
        self.source_mask: int = self._mask(self.source.start, size_src)
        self.size: int = size_src

        # Enforce constraints on the destination slice
        if self.destination is not None:
            self._validate_slice(self.destination)
            size_dst = self.destination.stop - self.destination.start + 1
            if size_src != size_dst:
                raise PyrisccoreAssertion(f"'source' and 'destination' slices must be the same size ({size_src} bits vs {size_dst} bits)")

            # Use the destination slice
            self.destination_mask: int = self._mask(self.destination.start, size_dst)

    @staticmethod
    def _validate_slice(s: slice):
        if s.start is None:
            raise PyrisccoreAssertion(f"'start' must be provided in the slice: {s}")
        if s.step is not None and s.step != 1:
            raise PyrisccoreAssertion(f"'step' must be 1 in the slice: {s}")
        if s.stop >= WORD.xlen or s.start >= WORD.xlen:
            raise PyrisccoreAssertion(f"'start' and 'stop' cannot exceed the architecture's XLEN in the slice: {s}")
        if s.start < 0 or s.stop < 0:
            raise PyrisccoreAssertion(f"'start' and 'stop' cannot be negative in the slice: {s}")

    @staticmethod
    def _mask(lsb: int, bit_length: int) -> int:
        """ return a mask isolating the value of this particular field
        """
        if bit_length <= 0:
            return 0
        return ((1 << bit_length) - 1) << lsb

    @staticmethod
    def _read(source: int, mask: int, lsb: int) -> int:
        """ read a value from a source given a mask and the least significant bit
        """
        return (source & mask) >> lsb

    @staticmethod
    def _write(value: int, mask: int, lsb: int, destination: int = 0, word: Word = WORD) -> int:
        """ write a value to a destination given a mask and the least significant bit
        """
        return (destination & (~mask & word.mask)) | (value << lsb)

    def read(self, source: int):
        """ return the value of this field given a source word
        """
        value = self._read(source, self.source_mask, self.source.start)

        if self.destination is None:
            return value

        return self._write(value, self.destination_mask, self.destination.start, 0)

    def write(self, value: int, destination: int = 0):
        """ return of the value of this field represented in a destination word
        """
        if self.destination is not None:
            value = self._read(value, self.destination_mask, self.destination.start)

        return self._write(value, self.source_mask, self.source.start, destination)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4