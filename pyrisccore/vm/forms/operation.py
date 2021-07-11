""" An "operation" is a named and numbered category of instructions with the same format
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Operation:
    """ A named and numbered category of instructions with the same format
    """

    format: str     # e.g. "I" for I-Type
    opcode: int     # e.g. 0b0110111
    name: str       # e.g. SYSTEM


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4