""" An "operation" is a named and numbered category of instructions with the same format
"""

from dataclasses import dataclass

from pyrisccore.vm.forms.format import Format


@dataclass
class Operation:
    """ A named and numbered category of instructions with the same format
    """

    format: Format  # e.g. I-Type
    opcode: int     # e.g. 0b0110111
    opname: str     # e.g. SYSTEM


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4