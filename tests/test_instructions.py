""" test the building blocks of instruction objects
"""

from pyrisccore.instructions import Field


def test_field_mask():

    # Case: 1-bit field starting at bit 0 (lsb)
    f = Field(0, 0)
    f.set(0b0001)  # 1 in the lsb
    assert f.value == 0b1

    # Case: 1-bit field starting at bit 1 (left of lsb)
    f = Field(1, 1)
    f.set(0b0010)
    assert f.value == 0b1

    # Case: 3-bit field starting at bit 2
    f = Field(2, 4)
    f.set(0b00010100)
    assert f.value == 0b101


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4