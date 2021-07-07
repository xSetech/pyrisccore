""" test the building blocks of an instruction
"""

from typing import List

import pytest

from pyrisccore import PyrisccoreAssertion
from pyrisccore.vm.forms.field import Field


def test_field_validate_slice():

    # Case: slice start and stop must be set
    with pytest.raises(PyrisccoreAssertion):
        Field._validate_slice(slice(0))

    # Case: slice start/stop must be positive
    with pytest.raises(PyrisccoreAssertion):
        Field._validate_slice(slice(-1, 0))
    with pytest.raises(PyrisccoreAssertion):
        Field._validate_slice(slice(0, -1))

    # Case: slice step must be 1 or None
    Field(slice(0, 0, 1))
    with pytest.raises(PyrisccoreAssertion):
        Field._validate_slice(slice(0, 0, 0))
    with pytest.raises(PyrisccoreAssertion):
        Field._validate_slice(slice(0, 0, 2))


@pytest.mark.parametrize(
    ["field", "word", "output"],
    [
        # Case: 1-bit field starting at bit 0 (lsb)
        [Field(source=slice(0, 0)), 0b0001, 0b1],

        # Case: 1-bit field starting at bit 1 (left of lsb)
        [Field(source=slice(1, 1)), 0b0010, 0b1],

        # Case: 3-bit field starting at bit 2
        [Field(source=slice(2, 4)), 0b00010100, 0b101],

    ]
)
def test_field_read_without_destination(field: Field, word: int, output: int):
    assert field.read(word) == output


@pytest.mark.parametrize(
    ["field", "args", "output"],
    [
        # Case: 1-valued 1-bit field starting at bit 0 (lsb)
        [Field(source=slice(0, 0)), [0b1, 0b0], 0b1],
        [Field(source=slice(0, 0)), [0b1, 0b1], 0b1],

        # Case: 1-valued 1-bit field starting at bit 1 (left of lsb)
        [Field(source=slice(1, 1)), [0b1, 0b000], 0b010],
        [Field(source=slice(1, 1)), [0b1, 0b001], 0b011],  # <- the one in the 0th position is preserved
        [Field(source=slice(1, 1)), [0b1, 0b100], 0b110],  # <- the one in the 2nd position is preserved

        # Case: 0-valued 1-bit field starting at bit 0 (lsb)
        # (just repeat the tests above with 0 as the value to place)
        [Field(source=slice(0, 0)), [0b0, 0b0], 0b0],
        [Field(source=slice(0, 0)), [0b0, 0b0], 0b0],
        [Field(source=slice(0, 0)), [0b0, 0b1], 0b0],

        # Case: 0-valued 1-bit field starting at bit 1 (left of lsb)
        [Field(source=slice(1, 1)), [0b0, 0b000], 0b000],
        [Field(source=slice(1, 1)), [0b0, 0b111], 0b101],
        [Field(source=slice(1, 1)), [0b0, 0b100], 0b100],

    ]
)
def test_field_write_without_destination(field: Field, args: List[int], output: int):
    assert field.write(*args) == output


@pytest.mark.parametrize(
    ["field", "word", "output"],
    [
        # Case: 1-bit field sourced from bit 0 (lsb) put at bit 0
        [Field(source=slice(0, 0), destination=slice(0, 0)), 0b1, 0b1],

        # Case: 1-bit field sourced from bit 1 (lsb) put at bit 0
        [Field(source=slice(1, 1), destination=slice(0, 0)), 0b10, 0b1],

        # Case: 1-bit field sourced from bit 2 (lsb) put at bit 3
        [Field(source=slice(2, 2), destination=slice(3, 3)), 0b100, 0b1000],

        # Case: 3-bit field sourced from bit 1 (lsb) put at bit 2
        [Field(source=slice(1, 3), destination=slice(2, 4)), 0b01110, 0b11100],

    ],
)
def test_field_read_with_destination(field: Field, word: int, output: int):
    assert field.read(word) == output


@pytest.mark.parametrize(
    ["field", "args", "output"],
    [
        # ! This is just the inverse of the tests above ^

        # Case: 1-bit field sourced from bit 0 (lsb) put at bit 0
        [Field(source=slice(0, 0), destination=slice(0, 0)), [0b1], 0b1],

        # Case: 1-bit field sourced from bit 1 (lsb) put at bit 0
        [Field(source=slice(1, 1), destination=slice(0, 0)), [0b1], 0b10],

        # Case: 1-bit field sourced from bit 2 (lsb) put at bit 3
        [Field(source=slice(2, 2), destination=slice(3, 3)), [0b1000], 0b100],

        # Case: 3-bit field sourced from bit 1 (lsb) put at bit 2
        [Field(source=slice(1, 3), destination=slice(2, 4)), [0b11100], 0b01110],

    ],
)
def test_field_write_with_destination(field: Field, args: List[int], output: int):
    assert field.write(*args) == output


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4