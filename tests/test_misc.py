""" Tests on the miscellaneous helper functions and objects
"""

import pytest

from pyrisccore.misc import (
    bit_count,
    frozendict,
    mask,
)


@pytest.mark.parametrize(
    ["d"],
    [
        [{}],
        [{'a': 1}],
        [{'b': [1, 2, 3]}],
        [{'x': 1, 'y': 2}],
        [{'y': 1, 'x': 2}],
    ]
)
def test_frozendict(d: dict):
    f = frozendict(d)

    # Confirm it's hashable
    hash(f)

    # Confirm keys are preserved
    assert d.keys() == f.keys()


@pytest.mark.parametrize(
    ["i", "count"],
    [
        [0b0000, 0],
        [0b0001, 1],
        [0b0010, 1],
        [0b0100, 1],
        [0b0101, 2],
        [0b1010, 2],
        [0b1110, 3],
        [0b1111, 4],
    ]
)
def test_bit_count(i, count):
    assert bit_count(i) == count


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