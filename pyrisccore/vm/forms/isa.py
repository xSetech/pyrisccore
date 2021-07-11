""" Instruction Set Architecture ("ISA") objects and interfaces
"""

from dataclasses import dataclass
from typing import Dict, Set

from pyrisccore.vm.forms.format import Format
from pyrisccore.vm.forms.operation import Operation
from pyrisccore.vm.forms.pseudoinstruction import PseudoInstruction
from pyrisccore.vm.forms.word import Word


@dataclass(frozen=True)
class ISA:
    """ An Instruction Set Architecture ("ISA")
    """

    # A short name for the ISA (e.g. "RV32I")
    name: str

    # A longer name for the ISA (e.g. "RISC-V 32-bit Base Integer Instruction Set")
    title: str

    # The definition of a word (e.g. Word(xlen=32) for 32-bit)
    word: Word

    # Instruction formats defining how slices of bits map to usable values.
    formats: Set[Format]

    # Named and numbered (by an "opcode") categories of instructions.
    operations: Set[Operation]

    # Mnemonics and constants for instruction encoding and decoding.
    pseudoinstructions: Set[PseudoInstruction]

    # Optional mnemonics and constants for instruction encoding and decoding.
    aliases: Dict[str, PseudoInstruction]


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4