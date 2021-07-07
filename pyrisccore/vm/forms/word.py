""" A "word" is an XLEN-sized collection of bits
"""


class Word:
    """ An "XLEN"-sized collection of bits
    """

    def __init__(self, xlen: int):
        self.xlen: int = xlen
        self.mask: int = (1 << xlen) - 1


WORD = Word(xlen = 32)  # e.g. 32 for "32-bit"


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4