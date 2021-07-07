""" An "instruction" is a named, numbered, and instanced operation on a virtual cpu core
"""

from pyrisccore.vm.forms.register import RegisterFile
from pyrisccore.vm.forms.pseudoinstruction import PseudoInstruction


class Instruction:
    """ A named, numbered, and instanced operation on a virtual cpu core
    """

    pseudo: PseudoInstruction  # e.g. "ADDI"

    def execute(self, rf: RegisterFile):
        raise NotImplementedError


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4