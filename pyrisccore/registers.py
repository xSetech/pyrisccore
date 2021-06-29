""" the register file
"""

from typing import Dict, List


class RegisterFile:
    """ Interface, storage, and behavior of the architectural registers

    RV32I specifies a minimum of two registers:
        - x0: constant zero read
        - pc: program counter

    Some "XLEN" number of registers sits between x0 and pc.
    These are the "general purpose" registers, by default there are 31.
    """

    def __init__(self, xlen: int = 31):

        # The number of general purpose registers.
        self.xlen: int = xlen

        # The values of all registers.
        self.file: List[int] = []

        # The mapping between register names and their position in the file.
        self.registers: Dict[str, int] = {}

        # The first register is the "zero" register; it will always read zero.
        # For debugging purposes, it will store whatever is written to it.
        self.file.append(0)
        self.registers["x0"] = 0

        # Extend the register file by the general purpose registers (x1, x2, etc)
        self.file.extend([0] * xlen)
        self.registers.update({f"x{n}": n for n in range(1, xlen + 1)})

        # The last register is (defined as via spec) the program counter.
        self.file.extend([0])
        self.registers["pc"] = len(self.file) - 1

    def load(self, register: str) -> int:
        """ Return the value mapped to a register, by its name (e.g. "x1", "pc")
        """
        # Special case:  x0 is always mapped to zero
        if register == "x0":
            return 0

        return self.file[self.registers[register]]

    def store(self, register: str, value: int) -> int:
        """ Map a value to a register, by its name (e.g. "x1"), returning the previous value
        """
        pos = self.registers[register]
        old = self.file[pos]
        self.file[pos] = value
        return old


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4