""" Slices of an instruction word that compose a distinct value
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple

from pyrisccore import PyrisccoreAssertion
from pyrisccore.vm.forms.word import WORD, Word


def bit_count(i: int) -> int:
    """ Count the set bits in an integer i

    Note: Python 3.10 introduced int.bit_count(); replace when it's released.
    """
    count = 0
    while i != 0:
        count += i & 0x1
        i >>= 1
    return count


@dataclass(
    frozen=False,       # <- __post_init__() will fail if this is True.
    unsafe_hash=True    # <- Once a Field is instantiated, it's effectively frozen.
)
class Field:
    """ A slice of an instruction word

    Example:

     0123456 789AB  <- bit index
    --------------
    |1100100|00000  <- values
    --------------
     ^^^^^^^        <- ex. "opcode" slice(0, 6) == 0b1100100
    """

    # The range of bits in a word for this field's value.
    source: slice
    source_mask: int = field(init=False)

    # The name of the field. Fields with the same name compose one Value from multiple slices.
    name: Optional[str] = None

    # Declare which of the source bits map to specific bits of the value.
    # For example, see the "imm" field of the J-Type instruction format.
    destination: Optional[slice] = None
    destination_mask: Optional[int] = field(init=False, default=None)

    # Number of bits required to represent this field's value.
    size: int = field(init=False)

    def __post_init__(self):

        # Enforce constraints on the source slice
        self._validate_slice(self.source)
        size_src = self.source.stop - self.source.start + 1

        # Use the source slice
        self.source_mask: int = self.mask(self.source.start, size_src)
        self.size: int = size_src

        # Enforce constraints on the destination slice
        if self.destination is not None:
            self._validate_slice(self.destination)
            size_dst = self.destination.stop - self.destination.start + 1
            if size_src != size_dst:
                raise PyrisccoreAssertion(f"'source' and 'destination' slices must be the same size ({size_src} bits vs {size_dst} bits)")

            # Use the destination slice
            self.destination_mask: int = self.mask(self.destination.start, size_dst)

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
    def mask(lsb: int, bit_length: int) -> int:
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

    def read(self, source: int) -> int:
        """ return the value of this field given a source word
        """
        value = self._read(source, self.source_mask, self.source.start)

        if self.destination is None:
            return value

        return self._write(value, self.destination_mask, self.destination.start, 0)

    def write(self, value: int, destination: int = 0) -> int:
        """ return of the value of this field represented in a destination word
        """
        if self.destination is not None:
            value = self._read(value, self.destination_mask, self.destination.start)

        return self._write(value, self.source_mask, self.source.start, destination)


@dataclass(
    frozen=False,       # <- __post_init__() will fail if this is True.
    unsafe_hash=True    # <- Once a Field is instantiated, it's effectively frozen.
)
class Value:
    """ One or more slices of an instruction word that make up a single value
    """

    fields: Tuple[Field, ...]
    name: Optional[str] = None

    source_mask: int = field(init=False)
    destination_mask: int = field(init=False)

    def __post_init__(self):

        # Constraint: This object works with one or more Field objects
        if not self.fields:
            raise PyrisccoreAssertion("One or more Field objects required")

        # Cast self.fields to a tuple if it's a list or another sequence.
        if not isinstance(self.fields, tuple):
            self.fields = tuple(self.fields)

        # Constraint: The sum of the sizes of the fields can't exceed XLEN
        if sum(f.size for f in self.fields) > WORD.xlen:
            raise PyrisccoreAssertion(f"A composition of Field objects can't exceed XLEN ({WORD.xlen}) size")

        # Constraint:
        #
        #   - One Field object makes reading a value simple: the source bits are
        #     are shifted to the lsb (bit 0) in the destination.
        #
        #   - Multiple Field objects require their source bits map explicitly to
        #     bits in the destination. This is to prevent bits in the source word
        #     from overwriting already-set bits in the destination.
        #
        if len(self.fields) > 1:
            for f in self.fields:
                if f.destination is None:
                    raise PyrisccoreAssertion(f"Field is required to have a destination slice for '{self.name}': {f}")

        # Compute the complete source and destination masks for this value.
        # Also check that Fields do not overlap in source or destination.
        self.source_mask = 0
        self.destination_mask = 0

        # A source->destination mapping isn't required for a single field.
        if len(self.fields) == 1:
            self.source_mask = self.fields[0].source_mask
            if self.fields[0].destination is None:
                self.destination_mask = Field.mask(0, self.fields[0].size)
            else:
                self.destination_mask = self.fields[0].destination_mask

        # ... an is essential for multiple fields.
        else:
            source_mask_bit_count = 0
            destination_mask_bits_count = 0
            for f in self.fields:
                self.source_mask |= f.source_mask
                self.destination_mask |= f.destination_mask
                if bit_count(self.source_mask) == source_mask_bit_count:
                    raise PyrisccoreAssertion(f"Field has overlapping source bits: {f}")
                if bit_count(self.destination_mask) == destination_mask_bits_count:
                    raise PyrisccoreAssertion(f"Field has overlapping destination bits: {f}")
                source_mask_bit_count = bit_count(self.source_mask)
                destination_mask_bits_count = bit_count(self.destination_mask)

    def read(self, source: int) -> int:
        """ return the value of this field given a source word
        """
        value = 0
        for f in self.fields:
            value |= f.read(source)
        return value

    def write(self, value: int, destination: int) -> int:
        """ return of the value of this field represented in a destination word
        """
        for f in self.fields:
            destination |= f.write(value, destination)
        return destination


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4