""" test the building blocks of an instruction
"""

from typing import List

import pytest

from pyrisccore import PyrisccoreAssertion
from pyrisccore.vm.forms.field import bit_count, Field, Value
from pyrisccore.vm.forms.slice import Slice


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


def test_field_invalid_inputs():

    # Case: source/destination are not the same size
    with pytest.raises(PyrisccoreAssertion):
        Field(source=Slice(0, 0), destination=Slice(0, 1))


def test_value_tuple_cast():

    # Case: Value will cast Value.field to a tuple.
    v = Value(fields=[Field(source=Slice(0,0))])
    assert isinstance(v.fields, tuple)


def test_value_invalid_inputs():

    # Case: Overlapping source bits
    with pytest.raises(PyrisccoreAssertion):
        Value(fields=[
            Field(source=Slice(0, 0), destination=Slice(1, 1)),
            Field(source=Slice(0, 0), destination=Slice(2, 2)),
        ])

    # Case: Overlapping destination bits
    with pytest.raises(PyrisccoreAssertion):
        Value(fields=[
            Field(source=Slice(1, 1), destination=Slice(0, 0)),
            Field(source=Slice(2, 2), destination=Slice(0, 0)),
        ])


@pytest.mark.parametrize(
    ["field", "word", "output"],
    [
        # Case: 1-bit field starting at bit 0 (lsb)
        [Field(source=Slice(0, 0)), 0b0001, 0b1],

        # Case: 1-bit field starting at bit 1 (left of lsb)
        [Field(source=Slice(1, 1)), 0b0010, 0b1],

        # Case: 3-bit field starting at bit 2
        [Field(source=Slice(2, 4)), 0b00010100, 0b101],

    ]
)
def test_field_read_without_destination(field: Field, word: int, output: int):
    assert field.get(word) == output


@pytest.mark.parametrize(
    ["field", "args", "output"],
    [
        # Case: 1-valued 1-bit field starting at bit 0 (lsb)
        [Field(source=Slice(0, 0)), [0b1, 0b0], 0b1],
        [Field(source=Slice(0, 0)), [0b1, 0b1], 0b1],

        # Case: 1-valued 1-bit field starting at bit 1 (left of lsb)
        [Field(source=Slice(1, 1)), [0b1, 0b000], 0b010],
        [Field(source=Slice(1, 1)), [0b1, 0b001], 0b011],  # <- the one in the 0th position is preserved
        [Field(source=Slice(1, 1)), [0b1, 0b100], 0b110],  # <- the one in the 2nd position is preserved

        # Case: 0-valued 1-bit field starting at bit 0 (lsb)
        # (just repeat the tests above with 0 as the value to place)
        [Field(source=Slice(0, 0)), [0b0, 0b0], 0b0],
        [Field(source=Slice(0, 0)), [0b0, 0b0], 0b0],
        [Field(source=Slice(0, 0)), [0b0, 0b1], 0b0],

        # Case: 0-valued 1-bit field starting at bit 1 (left of lsb)
        [Field(source=Slice(1, 1)), [0b0, 0b000], 0b000],
        [Field(source=Slice(1, 1)), [0b0, 0b111], 0b101],
        [Field(source=Slice(1, 1)), [0b0, 0b100], 0b100],

    ]
)
def test_field_write_without_destination(field: Field, args: List[int], output: int):
    assert field.set(*args) == output


@pytest.mark.parametrize(
    ["field", "word", "output"],
    [
        # Case: 1-bit field sourced from bit 0 (lsb) put at bit 0
        [Field(source=Slice(0, 0), destination=Slice(0, 0)), 0b1, 0b1],

        # Case: 1-bit field sourced from bit 1 (lsb) put at bit 0
        [Field(source=Slice(1, 1), destination=Slice(0, 0)), 0b10, 0b1],

        # Case: 1-bit field sourced from bit 2 (lsb) put at bit 3
        [Field(source=Slice(2, 2), destination=Slice(3, 3)), 0b100, 0b1000],

        # Case: 3-bit field sourced from bit 1 (lsb) put at bit 2
        [Field(source=Slice(1, 3), destination=Slice(2, 4)), 0b01110, 0b11100],

    ],
)
def test_field_read_with_destination(field: Field, word: int, output: int):
    assert field.get(word) == output


@pytest.mark.parametrize(
    ["field", "args", "output"],
    [
        # ! This is just the inverse of the tests above ^

        # Case: 1-bit field sourced from bit 0 (lsb) put at bit 0
        [Field(source=Slice(0, 0), destination=Slice(0, 0)), [0b1], 0b1],

        # Case: 1-bit field sourced from bit 1 (lsb) put at bit 0
        [Field(source=Slice(1, 1), destination=Slice(0, 0)), [0b1], 0b10],

        # Case: 1-bit field sourced from bit 2 (lsb) put at bit 3
        [Field(source=Slice(2, 2), destination=Slice(3, 3)), [0b1000], 0b100],

        # Case: 3-bit field sourced from bit 1 (lsb) put at bit 2
        [Field(source=Slice(1, 3), destination=Slice(2, 4)), [0b11100], 0b01110],

    ],
)
def test_field_write_with_destination(field: Field, args: List[int], output: int):
    assert field.set(*args) == output


@pytest.mark.parametrize(
    ["value", "word", "output"],
    [
        # Case: Value from a single 1-bit field
        [
            Value(fields=(
                Field(source=Slice(0, 0)),
            )),
            0b1, 0b1
        ],

        # Case: Value from a single 2-bit field
        [
            Value(fields=(
                Field(source=Slice(1, 2)),
            )),
            0b110, 0b11
        ],

        # Case: Value from/to multiple 1-bit fields
        [
            Value(fields=(
                Field(source=Slice(0, 0), destination=Slice(0, 0)),
                Field(source=Slice(2, 2), destination=Slice(1, 1)),
            )),
            0b101, 0b11
        ],

        # Case: Value from/to multiple 2-bit fields
        [
            Value(fields=(
                Field(source=Slice(0, 1), destination=Slice(0, 1)),
                Field(source=Slice(3, 4), destination=Slice(4, 5)),
            )),
            0b011011, 0b110011
        ],

    ]
)
def test_value_read(value: Value, word: int, output: int):
    assert value.get(word) == output


@pytest.mark.parametrize(
    ["value", "output", "word"],
    [
        # Case: Value from a single 1-bit field
        [
            Value(fields=(
                Field(source=Slice(0, 0)),
            )),
            0b1, 0b1
        ],

        # Case: Value from a single 2-bit field
        [
            Value(fields=(
                Field(source=Slice(1, 2)),
            )),
            0b110, 0b11
        ],

        # Case: Value from/to multiple 1-bit fields
        [
            Value(fields=(
                Field(source=Slice(0, 0), destination=Slice(0, 0)),
                Field(source=Slice(2, 2), destination=Slice(1, 1)),
            )),
            0b101, 0b11
        ],

        # Case: Value from/to multiple 2-bit fields
        [
            Value(fields=(
                Field(source=Slice(0, 1), destination=Slice(0, 1)),
                Field(source=Slice(3, 4), destination=Slice(4, 5)),
            )),
            0b011011, 0b110011
        ],

    ]
)
def test_value_write(value: Value, output: int, word: int):
    assert value.set(word, 0) == output


@pytest.mark.parametrize(
    ["value", "src_mask", "dst_mask"],
    [

        # Case: Value from a single 1-bit field
        [
            Value(fields=(
                Field(source=Slice(0, 0)),
            )),
            0b1, 0b1
        ],

        # Case: Value from a single 2-bit field
        [
            Value(fields=(
                Field(source=Slice(1, 2)),
            )),
            0b110, 0b11
        ],

        # Case: Value from/to multiple 1-bit fields
        [
            Value(fields=(
                Field(source=Slice(0, 0), destination=Slice(0, 0)),
                Field(source=Slice(2, 2), destination=Slice(1, 1)),
            )),
            0b101, 0b11
        ],

        # Case: Value from/to multiple 2-bit fields
        [
            Value(fields=(
                Field(source=Slice(0, 1), destination=Slice(0, 1)),
                Field(source=Slice(3, 4), destination=Slice(4, 5)),
            )),
            0b011011, 0b110011
        ],

    ]
)
def test_value_src_and_dst_masks(value: Value, src_mask: int, dst_mask: int):
    assert value.source_mask == src_mask
    assert value.destination_mask == dst_mask


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4