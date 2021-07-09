""" Slices of an instruction word that compose a distinct value
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple

from pyrisccore import PyrisccoreAssertion
from pyrisccore.misc import mask
from pyrisccore.vm.forms.slice import Slice


def bit_count(i: int) -> int:
    """ Count the set bits in an integer i

    Note: Python 3.10 introduced int.bit_count(); replace when it's released.
    """
    count = 0
    while i != 0:
        count += i & 0x1
        i >>= 1
    return count


@dataclass(frozen=True)
class Field:
    """ A mapping from the bits of an int to the bits of another
    """

    # The range of bits in a word for this field's value.
    source: Slice

    # The name of the field. Fields with the same name compose one Value from multiple slices.
    name: Optional[str] = None

    # Declare which of the source bits map to specific bits of the value.
    # For example, see the "imm" field of the J-Type instruction format.
    destination: Optional[Slice] = None

    def __post_init__(self):

        # Enforce constraints on the destination Slice
        if self.destination is not None:
            if self.source.length != self.destination.length:
                raise PyrisccoreAssertion("A Field's source and destination slices must be the same length")

    @property
    def length(self):
        return self.source.length

    def get(self, source: int) -> int:
        """ Get bits from an integer "source" according to this Field's bit-mapping
        """
        value = self.source.get(source)

        if self.destination is None:
            return value

        return self.destination.set(value, 0)

    def set(self, value: int, destination: int = 0) -> int:
        """ Set the bits in an integer "destination" to a "value" according to this Field's bit-mapping
        """
        if self.destination is not None:
            value = self.destination.get(value)

        return self.source.set(value, destination)


@dataclass(
    frozen=False,       # <- __post_init__() will fail if this is True.
    unsafe_hash=True    # <- This object is used as though it's actually read-only.
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
            self.source_mask = self.fields[0].source.mask
            if self.fields[0].destination is None:
                self.destination_mask = mask(0, self.fields[0].source.length)
            else:
                self.destination_mask = self.fields[0].destination.mask

        # ... and is essential for multiple fields.
        else:
            source_mask_bit_count = 0
            destination_mask_bits_count = 0
            for f in self.fields:
                self.source_mask |= f.source.mask
                self.destination_mask |= f.destination.mask
                if bit_count(self.source_mask) == source_mask_bit_count:
                    raise PyrisccoreAssertion(f"Field has overlapping source bits: {f}")
                if bit_count(self.destination_mask) == destination_mask_bits_count:
                    raise PyrisccoreAssertion(f"Field has overlapping destination bits: {f}")
                source_mask_bit_count = bit_count(self.source_mask)
                destination_mask_bits_count = bit_count(self.destination_mask)

    def get(self, source: int) -> int:
        """ Get bits from an integer "source" according to this Value's bit-mappings
        """
        value = 0
        for f in self.fields:
            value |= f.get(source)
        return value

    def set(self, value: int, destination: int) -> int:
        """ Set the bits in an integer "destination" to a "value" according to this Value's bit-mappings
        """
        for f in self.fields:
            destination |= f.set(value, destination)
        return destination


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4