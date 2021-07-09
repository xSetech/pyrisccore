""" Tests on the miscellaneous helper functions and objects
"""

import pytest

from pyrisccore.misc import mask


@pytest.mark.parametrize(
    ["lsb", "length", "output"],
    [
        [0, 0, 0b0000],
        [0, 1, 0b0001],
        [1, 1, 0b0010],
        [1, 2, 0b0110],
    ]
)
def test_mask(lsb: int, length: int, output: int):
    assert mask(lsb, length) == output


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4