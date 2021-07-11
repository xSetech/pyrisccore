""" A "word" is an XLEN-sized collection of bits
"""


class Word:
    """ An "XLEN"-sized collection of bits
    """

    def __init__(self, xlen: int):
        self.xlen: int = xlen
        self.mask: int = (1 << xlen) - 1


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4