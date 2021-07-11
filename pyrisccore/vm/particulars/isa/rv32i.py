""" RISC-V 32-bit Base Integer Instruction Set ("RV32I")

Opcodes, field names, mnemonics, etc cited from:
 - “The RISC-V Instruction Set Manual, Volume I: User-Level ISA, Document Version 20191213”,
 - Editors Andrew Waterman and Krste Asanovi ́c, RISC-V Foundation, December 2019.
 - https://github.com/riscv/riscv-isa-manual/releases/download/Ratified-IMAFDQC/riscv-spec-20191213.pdf
"""

from typing import Dict, Set

from pyrisccore.misc import frozendict
from pyrisccore.vm.forms.field import Field
from pyrisccore.vm.forms.format import Format
from pyrisccore.vm.forms.isa import ISA
from pyrisccore.vm.forms.operation import Operation
from pyrisccore.vm.forms.pseudoinstruction import PseudoInstruction
from pyrisccore.vm.forms.slice import Slice
from pyrisccore.vm.forms.word import Word


formats: Set[Format] = {

    Format(
        name="R",
        fields = (
            Field(Slice( 0,  6), "opcode"),
            Field(Slice( 7, 11), "rd"),
            Field(Slice(12, 14), "funct3"),
            Field(Slice(15, 19), "rs1"),
            Field(Slice(20, 24), "rs2"),
            Field(Slice(25, 31), "funct7"),
        )
    ),

    Format(
        name="I",
        fields = (
            Field(Slice( 0,  6), "opcode"),
            Field(Slice( 7, 11), "rd"),
            Field(Slice(12, 14), "funct3"),
            Field(Slice(15, 19), "rs1"),
            Field(Slice(20, 31), "imm", Slice(0, 11)),
        )
    ),

    Format(
        name="S",
        fields = (
            Field(Slice( 0,  6), "opcode"),
            Field(Slice( 7, 11), "imm", Slice(0, 4)),
            Field(Slice(12, 14), "funct3"),
            Field(Slice(15, 19), "rs1"),
            Field(Slice(20, 24), "rs2"),
            Field(Slice(25, 31), "imm", Slice(5, 11)),
        )
    ),

    Format(
        name="B",
        fields = (
            Field(Slice( 0,  6), "opcode"),
            Field(Slice( 7,  7), "imm", Slice(11, 11)),
            Field(Slice( 8, 11), "imm", Slice(1, 4)),
            Field(Slice(12, 14), "funct3"),
            Field(Slice(15, 19), "rs1"),
            Field(Slice(20, 24), "rs2"),
            Field(Slice(25, 30), "imm", Slice(5, 10)),
            Field(Slice(31, 31), "imm", Slice(12, 12)),
        )
    ),

    Format(
        name="U",
        fields = (
            Field(Slice( 0,  6), "opcode"),
            Field(Slice( 7, 11), "rd"),
            Field(Slice(12, 31), "imm", Slice(12, 31)),
        )
    ),

    Format(
        name="J",
        fields = (
            Field(Slice( 0,  6), "opcode"),
            Field(Slice( 7, 11), "rd"),
            Field(Slice(12, 19), "imm", Slice(12, 19)),
            Field(Slice(20, 20), "imm", Slice(11, 11)),
            Field(Slice(21, 30), "imm", Slice(1, 10)),
            Field(Slice(31, 31), "imm", Slice(20, 20)),
        )
    ),

}


# opcode -> Operation
operations: Set[Operation] = {

    Operation(format="I", opcode=0b0010011, name="OP-IMM"),
    Operation(format="U", opcode=0b0110111, name="LUI"),
    Operation(format="U", opcode=0b0010111, name="AUIPC"),
    Operation(format="R", opcode=0b0110011, name="OP"),
    Operation(format="J", opcode=0b1101111, name="JAL"),
    Operation(format="I", opcode=0b1100111, name="JALR"),
    Operation(format="B", opcode=0b1100011, name="BRANCH"),
    Operation(format="I", opcode=0b0000011, name="LOAD"),
    Operation(format="S", opcode=0b0100011, name="STORE"),
    Operation(format="I", opcode=0b0001111, name="MISC-MEM"),
    Operation(format="I", opcode=0b1110011, name="SYSTEM"),

}


pseudoinstructions: Set[PseudoInstruction] = {

    # Register-Immediate

    PseudoInstruction("ADDI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b000,
        }),
    ),
    PseudoInstruction("SLTI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b010,
        }),
    ),
    PseudoInstruction("SLTIU", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b011,
        }),
    ),
    PseudoInstruction("ANDI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b111,
        }),
    ),
    PseudoInstruction("ORI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b000,
        }),
    ),
    PseudoInstruction("XORI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b000,
        }),
    ),
    PseudoInstruction("SLLI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b001,
            Field(Slice(25, 31), "imm", Slice(5, 11)): 0b0000000,
        }),
        subfields=(
            Field(Slice(20, 24), "shamt"),
        ),
    ),
    PseudoInstruction("SRLI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b101,
            Field(Slice(25, 31), "imm", Slice(5, 11)): 0,
        }),
        subfields=(
            Field(Slice(20, 24), "shamt"),
        ),
    ),
    PseudoInstruction("SRAI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b101,
            Field(Slice(25, 31), "imm", Slice(5, 11)): 0b0100000,
        }),
        subfields=(
            Field(Slice(20, 24), "shamt"),
        ),
    ),
    PseudoInstruction("LUI", operation="LUI"),
    PseudoInstruction("AUIPC", operation="AUIPC"),

    # Register-Register

    PseudoInstruction("ADD", operation="OP",
        constants=frozendict({
            "funct3": 0b000,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("SLT", operation="OP",
        constants=frozendict({
            "funct3": 0b010,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("SLTU", operation="OP",
        constants=frozendict({
            "funct3": 0b011,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("AND", operation="OP",
        constants=frozendict({
            "funct3": 0b111,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("OR", operation="OP",
        constants=frozendict({
            "funct3": 0b110,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("XOR", operation="OP",
        constants=frozendict({
            "funct3": 0b100,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("SLL", operation="OP",
        constants=frozendict({
            "funct3": 0b001,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("SRL", operation="OP",
        constants=frozendict({
            "funct3": 0b101,
            "funct7": 0,
        }),
    ),
    PseudoInstruction("SUB", operation="OP",
        constants=frozendict({
            "funct3": 0b000,
            "funct7": 0b0100000,
        }),
    ),
    PseudoInstruction("SRA", operation="OP",
        constants=frozendict({
            "funct3": 0b101,
            "funct7": 0b0100000,
        }),
    ),

    # Unconditional Jumps

    PseudoInstruction("JAL", operation="JAL",
        subfields=(
            Field(Slice(12, 31), "offset", Slice(1, 20)),
        )
    ),
    PseudoInstruction("JALR", operation="JALR",
        subfields=(
            Field(Slice(20, 31), "offset", Slice(0, 11)),
        )
    ),

    # Conditional Branches

    PseudoInstruction("BEQ", operation="BRANCH",
        constants=frozendict({
            "funct3": 0b000,
        }),
    ),
    PseudoInstruction("BNE", operation="BRANCH",
        constants=frozendict({
            "funct3": 0b001,
        }),
    ),
    PseudoInstruction("BLT", operation="BRANCH",
        constants=frozendict({
            "funct3": 0b100,
        }),
    ),
    PseudoInstruction("BLTU", operation="BRANCH",
        constants=frozendict({
            "funct3": 0b110,
        }),
    ),
    PseudoInstruction("BGE", operation="BRANCH",
        constants=frozendict({
            "funct3": 0b101,
        }),
    ),
    PseudoInstruction("BGEU", operation="BRANCH",
        constants=frozendict({
            "funct3": 0b111,
        }),
    ),

    # Load and Store

    PseudoInstruction("LB", operation="LOAD",
        constants=frozendict({
            "funct3": 0b000,
        }),
    ),
    PseudoInstruction("LH", operation="LOAD",
        constants=frozendict({
            "funct3": 0b001,
        }),
    ),
    PseudoInstruction("LW", operation="LOAD",
        constants=frozendict({
            "funct3": 0b010,
        }),
    ),
    PseudoInstruction("LBU", operation="LOAD",
        constants=frozendict({
            "funct3": 0b100,
        }),
    ),
    PseudoInstruction("LHU", operation="LOAD",
        constants=frozendict({
            "funct3": 0b101,
        }),
    ),
    PseudoInstruction("SB", operation="STORE",
        constants=frozendict({
            "funct3": 0b000,
        }),
    ),
    PseudoInstruction("SH", operation="STORE",
        constants=frozendict({
            "funct3": 0b001,
        }),
    ),
    PseudoInstruction("SW", operation="STORE",
        constants=frozendict({
            "funct3": 0b010,
        }),
    ),

    # Memory Ordering

    PseudoInstruction("FENCE", operation="MISC-MEM",
        constants=frozendict({
            "rd": 0,
            "rs1": 0,
        }),
        subfields=(
            Field(Slice(20, 20), "SW"),
            Field(Slice(21, 21), "SR"),
            Field(Slice(22, 22), "SO"),
            Field(Slice(23, 23), "SI"),
            Field(Slice(24, 24), "PW"),
            Field(Slice(25, 25), "PR"),
            Field(Slice(26, 26), "PO"),
            Field(Slice(27, 27), "PI"),
            Field(Slice(28, 31), "fm"),
        ),
    ),

    # Environment Call and Breakpoints

    PseudoInstruction("ECALL", operation="SYSTEM",
        constants=frozendict({
            "rd": 0,
            "rs1": 0,
            "funct3": 0b000,  # PRIV
            "imm": 0b000,
        }),
        subfields=(
            Field(Slice(20, 20), "SW"),
            Field(Slice(21, 21), "SR"),
            Field(Slice(22, 22), "SO"),
            Field(Slice(23, 23), "SI"),
            Field(Slice(24, 24), "PW"),
            Field(Slice(25, 25), "PR"),
            Field(Slice(26, 26), "PO"),
            Field(Slice(27, 27), "PI"),
            Field(Slice(28, 31), "fm"),
        ),
    ),
    PseudoInstruction("EBREAK", operation="SYSTEM",
        constants=frozendict({
            "rd": 0,
            "rs1": 0,
            "funct3": 0b000,  # PRIV
            "imm": 0b000,
        }),
        subfields=(
            Field(Slice(20, 20), "SW"),
            Field(Slice(21, 21), "SR"),
            Field(Slice(22, 22), "SO"),
            Field(Slice(23, 23), "SI"),
            Field(Slice(24, 24), "PW"),
            Field(Slice(25, 25), "PR"),
            Field(Slice(26, 26), "PO"),
            Field(Slice(27, 27), "PI"),
            Field(Slice(28, 31), "fm"),
        ),
    ),

}


aliases: Dict[str, PseudoInstruction] = frozendict({
    "NOP": PseudoInstruction("ADDI", operation="OP-IMM",
        constants=frozendict({
            "funct3": 0b000,
            "imm": 0,
        }),
    ),
})


RV32I = ISA(
    name="RV32I",
    title="RISC-V 32-bit Base Integer Instruction Set",
    word=Word(xlen=32),
    formats=formats,
    operations=operations,
    pseudoinstructions=pseudoinstructions,
    aliases=aliases,
)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4