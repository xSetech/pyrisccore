""" instruction building blocks

You know how you're used to reading arrays left to right, with the left most
thing in the array being the 0th position? This is the reverse. The furthest
right position is now the 0th.

This applies to elements in a list too!

Chunks of the bits representation ("fields") are given in right -> left order
because of this. In any Python list, index 0 corresponds to the
object closest to the MSB. This makes concatenation easy.

Integers haven't changed, though. The bit on the right has always been the least
significant bit and it doesn't change in this code. In other words, 0x0001 is 1.
"""

from dataclasses import dataclass
from struct import iter_unpack, pack, unpack
from typing import Dict, List, Optional, Tuple, Type

from pyrisccore.registers import RegisterFile


class Field:
    """ a slice of a 64-bit value
    """

    value: int

    def __init__(self, lsb: int, msb: int):
        self.lsb: int = lsb
        self.msb: int = msb
        self.size: int = msb - lsb + 1
        self.mask: int = self._mask(lsb, self.size)

    @staticmethod
    def _mask(lsb: int, size: int) -> int:
        """ return a mask given the starting position and quantity of 1s
        """
        if size == 0:
            return 0
        mask = 0
        for i in range(size + lsb):
            mask <<= 1
            if i < size:
                mask += 1
        return mask

    def set(self, word: int):
        """ set the value of the field from a 64-bit word
        """
        self.value = (word & self.mask) >> self.lsb


class Format:
    """ an instruction format that translates to/from binary/fields
    """

    # All instruction formats define fields by their bounds.
    fields: Tuple[Field, ...]

    def encode(self, fields: Tuple[int, ...]) -> int:
        """ return the packed bit representation of multiple fields
        """
        raise NotImplementedError  # TODO

    def decode(self, word: int) -> Tuple[int, ...]:
        """ unpack the bits representation of an instruction format
        """
        raise NotImplementedError  # TODO


class RType(Format):

    fields = (
        Field( 0,  6),  # opcode
        Field( 7, 11),  # rd
        Field(12, 14),  # funct3
        Field(15, 19),  # rs1
        Field(20, 24),  # rs2
        Field(25, 31),  # funct7
    )


class IType(Format):

    fields = (
        Field( 0,  6),  # opcode
        Field( 7, 11),  # rd
        Field(12, 14),  # funct3
        Field(15, 19),  # rs1
        Field(20, 31),  # imm[0:11]
    )


class SType(Format):

    fields = (
        Field( 0,  6),  # opcode
        Field( 7, 11),  # imm[0:4]
        Field(12, 14),  # funct3
        Field(15, 19),  # rs1
        Field(20, 24),  # rs2
        Field(25, 31),  # imm[5:11]
    )


class BType(Format):

    fields = (
        Field( 0,  6),  # opcode
        Field( 7,  7),  # imm[11]
        Field( 8, 11),  # imm[1:4]
        Field(12, 14),  # funct3
        Field(15, 19),  # rs1
        Field(20, 24),  # rs2
        Field(25, 30),  # imm[5:10]
        Field(31, 31),  # imm[12]
    )


class UType(Format):

    fields = (
        Field( 0,  6),  # opcode
        Field( 7, 11),  # rd
        Field(12, 31),  # imm [12:31]
    )


class JType(Format):

    fields = (
        Field( 0,  6),  # opcode
        Field( 7, 11),  # rd
        Field(12, 19),  # imm[12:19]
        Field(20, 20),  # imm[11]
        Field(21, 30),  # imm[1:10]
        Field(31, 31),  # imm[20]
    )


class Instruction:

    # These class attributes are defined by the various subclasses
    opcode: int
    format: Format

    # The 64-bit representation of the instruction
    value: int

    def __init__(self, *fields, value: Optional[int]):

        # Most of the time, the VM is decoding binary into instructions.
        # In this case, we can avoid the work of computing the instructions
        # binary representation by just saving the source material.
        #
        # Otherwise compute it from the instruction format fields (in the case
        # of e.g. mnemonic or unit tests).
        self.value = value if value is not None else self.format.encode(*fields)

    def execute(self, rf: RegisterFile):
        """ execute the instruction against the state machine
        """
        raise NotImplementedError


class Decoder:
    """ binary instructions -> instruction objects
    """

    # Put available instructions here, by class:
    instruction_classes: Tuple[Type[Instruction]] = (
        # ...
    )

    # A mapping from opcode to Instruction class that is created at runtime and
    # used to quickly decode bits to a particular instruction.
    instruction_classes_by_opcode: Dict[int, Type[Instruction]]

    def __init__(self):

        # Create the mapping from opcode to Instruction class
        self.instruction_classes_by_opcode = {}
        for instruction_class in self.instruction_classes:
            self.instruction_classes_by_opcode[instruction_class.opcode] = instruction_class

    def decode(self, word: int) -> Instruction:
        """ Decode 64 bits into an Instruction object
        """
        opcode = word & 0x3f  # 6 bits
        instruction_class = self.instruction_classes_by_opcode[opcode]
        instruction_fields = instruction_class.format.decode(word)
        return instruction_class(*instruction_fields, value=word)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4