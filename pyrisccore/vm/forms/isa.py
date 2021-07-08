""" Instruction Set Architecture ("ISA") objects and interfaces
"""

from dataclasses import dataclass
from typing import Dict

from pyrisccore.vm.forms.format import Format
from pyrisccore.vm.forms.operation import Operation
from pyrisccore.vm.forms.pseudoinstruction import PseudoInstruction


@dataclass(frozen=False)
class ISA:
    """ An Instruction Set Architecture ("ISA")
    """

    # A short name for the ISA (e.g. "RV32I")
    name: str

    # A longer name for the ISA (e.g. "RISC-V 32-bit Base Integer Instruction Set")
    title: str

    # The length of a word (e.g. 32 for 32-bit)
    xlen: int

    # Instruction formats defining how slices of bits map to usable values.
    # Mapping: instruction format letter -> Format (e.g. J -> Format for "J-Type")
    formats: Dict[str, Format]

    # Named and numbered (by an "opcode") categories of instructions.
    # Mapping: operation name -> Operation (e.g. "OP-IMM" -> Operation for "OP-IMM")
    operations: Dict[int, Operation]

    # Mnemonics and constants for instruction encoding and decoding.
    # Mapping: mnemonic -> PseudoInstruction (e.g. "ADDI" -> PseudoInstruction for "ADDI")
    pseudoinstructions: Dict[str, PseudoInstruction]

    # Optional mnemonics and constants for instruction encoding and decoding.
    # Mapping: mnemonic -> PseudoInstruction (e.g. "NOP" -> PseudoInstruction for "ADDI x0 0")
    aliases: Dict[str, PseudoInstruction]


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4