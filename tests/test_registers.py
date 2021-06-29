""" test the register file
"""

from pyrisccore.registers import RegisterFile


def test_init():
    """ test that default parameters don't cause an exception
    """
    RegisterFile()


def test_register_naming():
    """ test that register names map to expected positions and then to expected values
    """
    # Case:  default xlen value
    rf = RegisterFile()
    assert rf.registers["x0"] == 0
    assert rf.registers["pc"] == len(rf.file) - 1

    # ... and, that they're initialized to zero
    assert rf.file[rf.registers["x0"]] == 0
    assert rf.file[rf.registers["pc"]] == 0

    # Case:  2 general purpose registers
    rf = RegisterFile(xlen=2)
    assert rf.registers["x0"] == 0
    assert rf.registers["x1"] == 1
    assert rf.registers["x2"] == 2
    assert rf.registers["pc"] == 3

    # Reminder to account for special registers, above :)
    assert len(rf.registers.keys()) == rf.xlen + 2


def test_load():
    """ RegisterFile.load() basic tests
    """
    rf = RegisterFile(xlen=2)

    # Case:  x0 returns zero
    assert rf.load("x0") == 0


def test_store():
    """ RegisterFile.store() basic tests
    """
    rf = RegisterFile(xlen=2)

    # Case: x0 permits a non-zero store operation (blackhole for data)
    rf.store("x0", 0x1)

    # Case: Storing to a general purpose register
    rf.store("x1", 0x2)

    # Case: Storing to the program counter is permitted
    rf.store("pc", 0x3)


def test_load_and_store():
    """ RegisterFile.load() + RegisterFile.store() tests
    """
    rf = RegisterFile(xlen=2)

    # Case: x0 permits a non-zero store operation (blackhole for data).
    #       This does not affect the returned value from a load.
    assert rf.load("x0") == 0x0
    assert rf.store("x0", 0x2) == 0x0
    assert rf.load("x0") == 0x0

    # ... but, note that the store() method returns the previous stored value.
    # This is only meant to be visible internally, for debugging.
    assert rf.store("x0", 0x9) == 0x2
    assert rf.load("x0") == 0x0  # the load continues to be unaffected

    # Case: Storing/Loading to/from a general purpose register
    assert rf.load("x1") == 0x0
    assert rf.store("x1", 0x2) == 0x0
    assert rf.load("x1") == 0x2

    # Case: Storing/Loading to/from a general purpose register is permitted.
    assert rf.load("pc") == 0x0
    assert rf.store("pc", 0x3) == 0x0
    assert rf.load("pc") == 0x3


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4