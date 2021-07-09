""" Test pyrisccore.vm.forms.slice
"""

import pytest

from pyrisccore import PyrisccoreAssertion
from pyrisccore.vm.forms.slice import Slice


def test_input_validation():

    # Case: start and stop cannot be negative
    with pytest.raises(PyrisccoreAssertion):
        Slice(start=-1, stop=0)
    with pytest.raises(PyrisccoreAssertion):
        Slice(start=0, stop=-1)

    # Case: start must be less than or equal to stop
    with pytest.raises(PyrisccoreAssertion):
        Slice(start=1, stop=0)


def test_hash_and_compare():

    # Hashing
    hash(Slice(0, 0))
    assert hash(Slice(0, 0)) == hash(Slice(0, 0))
    assert hash(Slice(0, 0)) != hash(Slice(0, 1))
    assert hash(Slice(0, 0)) != hash(Slice(1, 1))

    # Comparison
    assert Slice(0, 0) == Slice(0, 0)
    assert Slice(0, 1) == Slice(0, 1)
    assert Slice(1, 1) == Slice(1, 1)


@pytest.mark.parametrize(
    ["s", "source", "output"],
    [
        # Case: 1-bit field starting at bit 0 (lsb)
        [Slice(0, 0), 0b0001, 0b1],

        # Case: 1-bit field starting at bit 1 (left of lsb)
        [Slice(1, 1), 0b0010, 0b1],

        # Case: 3-bit field starting at bit 2
        [Slice(2, 4), 0b00010100, 0b101],

    ]
)
def test_get(s: Slice, source: int, output: int):
    assert s.get(source) == output


@pytest.mark.parametrize(
    ["s", "value", "destination", "output"],
    [
        # Case: 1-valued 1-bit field starting at bit 0 (lsb)
        [Slice(0, 0), 0b1, 0b0, 0b1],
        [Slice(0, 0), 0b1, 0b1, 0b1],

        # Case: 1-valued 1-bit field starting at bit 1 (left of lsb)
        [Slice(1, 1), 0b1, 0b000, 0b010],
        [Slice(1, 1), 0b1, 0b001, 0b011],  # <- the one in the 0th position is preserved
        [Slice(1, 1), 0b1, 0b100, 0b110],  # <- the one in the 2nd position is preserved

        # Case: 0-valued 1-bit field starting at bit 0 (lsb)
        # (just repeat the tests above with 0 as the value to place)
        [Slice(0, 0), 0b0, 0b0, 0b0],
        [Slice(0, 0), 0b0, 0b0, 0b0],
        [Slice(0, 0), 0b0, 0b1, 0b0],

        # Case: 0-valued 1-bit field starting at bit 1 (left of lsb)
        [Slice(1, 1), 0b0, 0b000, 0b000],
        [Slice(1, 1), 0b0, 0b111, 0b101],
        [Slice(1, 1), 0b0, 0b100, 0b100],

    ]
)
def test_set(s: Slice, value: int, destination: int, output: int):
    assert s.set(value, destination) == output


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4