""" A "pseudo-instruction" is a mnemonic corresponding to the constant value of specific fields
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple, Union

from pyrisccore.vm.forms.field import Field
from pyrisccore.vm.forms.format import Format
from pyrisccore.vm.forms.operation import Operation


@dataclass
class PseudoInstruction:
    """ A mnemonic corresponding to the constant value of specific fields
    """

    mnemonic: str               # e.g. "ADDI"
    operation: Operation        # e.g. OP-IMM, gives the instruction format & opcode
    constants: Dict[Union[Field, str], int] = field(default_factory=dict)  # e.g. "funct3": 0b000 for "ADDI"
    subfields: Tuple[Format] = tuple()   # e.g. "shamt", derived from imm


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4