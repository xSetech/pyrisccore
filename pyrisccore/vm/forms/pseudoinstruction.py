""" A "pseudo-instruction" is a mnemonic corresponding to the constant value of specific fields
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple, Union

from pyrisccore.misc import frozendict
from pyrisccore.vm.forms.field import Field


@dataclass(frozen=True)
class PseudoInstruction:
    """ A mnemonic corresponding to the constant value of specific fields
    """

    mnemonic: str               # e.g. "ADDI"
    operation: str              # e.g. "OP-IMM", gives the instruction format & opcode
    constants: Dict[Union[Field, str], int] = field(default_factory=frozendict)  # e.g. "funct3": 0b000 for "ADDI"
    subfields: Tuple[Field] = tuple()   # e.g. "shamt", derived from imm


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4