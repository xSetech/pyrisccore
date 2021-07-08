""" RISC-V 32-bit Base Integer Instruction Set ("RV32I")

Opcodes, field names, mnemonics, etc cited from:
 - “The RISC-V Instruction Set Manual, Volume I: User-Level ISA, Document Version 20191213”,
 - Editors Andrew Waterman and Krste Asanovi ́c, RISC-V Foundation, December 2019.
 - https://github.com/riscv/riscv-isa-manual/releases/download/Ratified-IMAFDQC/riscv-spec-20191213.pdf
"""

from typing import Dict

from pyrisccore.vm.forms.field import Field
from pyrisccore.vm.forms.format import Format
from pyrisccore.vm.forms.operation import Operation
from pyrisccore.vm.forms.pseudoinstruction import PseudoInstruction


# instruction format letter -> Format
formats: Dict[str, Format] = {

    "R": Format(
        name="R",
        fields = (
            Field(slice( 0,  6), "opcode"),
            Field(slice( 7, 11), "rd"),
            Field(slice(12, 14), "funct3"),
            Field(slice(15, 19), "rs1"),
            Field(slice(20, 24), "rs2"),
            Field(slice(25, 31), "funct7"),
        )
    ),

    "I": Format(
        name="I",
        fields = (
            Field(slice( 0,  6), "opcode"),
            Field(slice( 7, 11), "rd"),
            Field(slice(12, 14), "funct3"),
            Field(slice(15, 19), "rs1"),
            Field(slice(20, 31), "imm", slice(0, 11)),
        )
    ),

    "S": Format(
        name="S",
        fields = (
            Field(slice( 0,  6), "opcode"),
            Field(slice( 7, 11), "imm", slice(0, 4)),
            Field(slice(12, 14), "funct3"),
            Field(slice(15, 19), "rs1"),
            Field(slice(20, 24), "rs2"),
            Field(slice(25, 31), "imm", slice(5, 11)),
        )
    ),

    "B": Format(
        name="B",
        fields = (
            Field(slice( 0,  6), "opcode"),
            Field(slice( 7,  7), "imm", slice(11, 11)),
            Field(slice( 8, 11), "imm", slice(1, 4)),
            Field(slice(12, 14), "funct3"),
            Field(slice(15, 19), "rs1"),
            Field(slice(20, 24), "rs2"),
            Field(slice(25, 30), "imm", slice(5, 10)),
            Field(slice(31, 31), "imm", slice(12)),
        )
    ),

    "U": Format(
        name="U",
        fields = (
            Field(slice( 0,  6), "opcode"),
            Field(slice( 7, 11), "rd"),
            Field(slice(12, 31), "imm", slice(12, 31)),
        )
    ),

    "J": Format(
        name="J",
        fields = (
            Field(slice( 0,  6), "opcode"),
            Field(slice( 7, 11), "rd"),
            Field(slice(12, 19), "imm", slice(12, 19)),
            Field(slice(20, 20), "imm", slice(11, 11)),
            Field(slice(21, 30), "imm", slice(1, 10)),
            Field(slice(31, 31), "imm", slice(20, 20)),
        )
    ),

}


# opcode -> Operation
operations: Dict[int, Operation] = {

    "OP-IMM":   Operation(formats["I"], 0b0010011, "OP-IMM"),
    "LUI":      Operation(formats["U"], 0b0110111, "LUI"),
    "AUIPC":    Operation(formats["U"], 0b0010111, "AUIPC"),
    "OP":       Operation(formats["R"], 0b0110011, "OP"),
    "JAL":      Operation(formats["J"], 0b1101111, "JAL"),
    "JALR":     Operation(formats["I"], 0b1100111, "JALR"),
    "BRANCH":   Operation(formats["B"], 0b1100011, "BRANCH"),
    "LOAD":     Operation(formats["I"], 0b0000011, "LOAD"),
    "STORE":    Operation(formats["S"], 0b0100011, "STORE"),
    "MISC-MEM": Operation(formats["I"], 0b0001111, "MISC-MEM"),
    "SYSTEM":   Operation(formats["I"], 0b1110011, "SYSTEM"),

}


# mnemonic -> PseudoInstruction
pseudoinstructions: Dict[str, PseudoInstruction] = {

    # Register-Immediate

    "ADDI": PseudoInstruction("ADDI", operations["OP-IMM"],
        constants={
            "funct3": 0b000,
        },
    ),
    "SLTI": PseudoInstruction("SLTI", operations["OP-IMM"],
        constants={
            "funct3": 0b010,
        },
    ),
    "SLTIU": PseudoInstruction("SLTIU", operations["OP-IMM"],
        constants={
            "funct3": 0b011,
        },
    ),
    "ANDI": PseudoInstruction("ANDI", operations["OP-IMM"],
        constants={
            "funct3": 0b111,
        },
    ),
    "ORI": PseudoInstruction("ORI", operations["OP-IMM"],
        constants={
            "funct3": 0b000,
        },
    ),
    "XORI": PseudoInstruction("XORI", operations["OP-IMM"],
        constants={
            "funct3": 0b000,
        },
    ),
    "SLLI": PseudoInstruction("SLLI", operations["OP-IMM"],
        constants={
            "funct3": 0b001,
            Field(slice(25, 31), "imm", slice(5, 11)): 0b0000000,
        },
        subfields=(
            Field(slice(20, 24), "shamt"),
        ),
    ),
    "SRLI": PseudoInstruction("SRLI", operations["OP-IMM"],
        constants={
            "funct3": 0b101,
            Field(slice(25, 31), "imm", slice(5, 11)): 0,
        },
        subfields=(
            Field(slice(20, 24), "shamt"),
        ),
    ),
    "SRAI": PseudoInstruction("SRAI", operations["OP-IMM"],
        constants={
            "funct3": 0b101,
            Field(slice(25, 31), "imm", slice(5, 11)): 0b0100000,
        },
        subfields=(
            Field(slice(20, 24), "shamt"),
        ),
    ),
    "LUI": PseudoInstruction("LUI", operations["LUI"]),
    "AUIPC": PseudoInstruction("AUIPC", operations["AUIPC"]),

    # Register-Register

    "ADD": PseudoInstruction("ADD", operations["OP"],
        constants={
            "funct3": 0b000,
            "funct7": 0,
        },
    ),
    "SLT": PseudoInstruction("SLT", operations["OP"],
        constants={
            "funct3": 0b010,
            "funct7": 0,
        },
    ),
    "SLTU": PseudoInstruction("SLTU", operations["OP"],
        constants={
            "funct3": 0b011,
            "funct7": 0,
        },
    ),
    "AND": PseudoInstruction("AND", operations["OP"],
        constants={
            "funct3": 0b111,
            "funct7": 0,
        },
    ),
    "OR": PseudoInstruction("OR", operations["OP"],
        constants={
            "funct3": 0b110,
            "funct7": 0,
        },
    ),
    "XOR": PseudoInstruction("XOR", operations["OP"],
        constants={
            "funct3": 0b100,
            "funct7": 0,
        },
    ),
    "SLL": PseudoInstruction("SLL", operations["OP"],
        constants={
            "funct3": 0b001,
            "funct7": 0,
        },
    ),
    "SRL": PseudoInstruction("SRL", operations["OP"],
        constants={
            "funct3": 0b101,
            "funct7": 0,
        },
    ),
    "SUB": PseudoInstruction("SUB", operations["OP"],
        constants={
            "funct3": 0b000,
            "funct7": 0b0100000,
        },
    ),
    "SRA": PseudoInstruction("SRA", operations["OP"],
        constants={
            "funct3": 0b101,
            "funct7": 0b0100000,
        },
    ),

    # Unconditional Jumps

    "JAL": PseudoInstruction("JAL", operations["JAL"],
        subfields=(
            Field(slice(12, 31), "offset", slice(1, 20)),
        )
    ),
    "JALR": PseudoInstruction("JALR", operations["JALR"],
        subfields=(
            Field(slice(20, 31), "offset", slice(0, 11)),
        )
    ),

    # Conditional Branches

    "BEQ": PseudoInstruction("BEQ", operations["BRANCH"],
        constants={
            "funct3": 0b000,
        },
    ),
    "BNE": PseudoInstruction("BNE", operations["BRANCH"],
        constants={
            "funct3": 0b001,
        },
    ),
    "BLT": PseudoInstruction("BLT", operations["BRANCH"],
        constants={
            "funct3": 0b100,
        },
    ),
    "BLTU": PseudoInstruction("BLTU", operations["BRANCH"],
        constants={
            "funct3": 0b110,
        },
    ),
    "BGE": PseudoInstruction("BGE", operations["BRANCH"],
        constants={
            "funct3": 0b101,
        },
    ),
    "BGEU": PseudoInstruction("BGEU", operations["BRANCH"],
        constants={
            "funct3": 0b111,
        },
    ),

    # Load and Store

    "LB": PseudoInstruction("LB", operations["LOAD"],
        constants={
            "funct3": 0b000,
        }
    ),
    "LH": PseudoInstruction("LH", operations["LOAD"],
        constants={
            "funct3": 0b001,
        }
    ),
    "LW": PseudoInstruction("LW", operations["LOAD"],
        constants={
            "funct3": 0b010,
        }
    ),
    "LBU": PseudoInstruction("LBU", operations["LOAD"],
        constants={
            "funct3": 0b100,
        }
    ),
    "LHU": PseudoInstruction("LHU", operations["LOAD"],
        constants={
            "funct3": 0b101,
        }
    ),
    "SB": PseudoInstruction("SB", operations["STORE"],
        constants={
            "funct3": 0b000,
        }
    ),
    "SH": PseudoInstruction("SH", operations["STORE"],
        constants={
            "funct3": 0b001,
        }
    ),
    "SW": PseudoInstruction("SW", operations["STORE"],
        constants={
            "funct3": 0b010,
        }
    ),

    # Memory Ordering

    "FENCE": PseudoInstruction("FENCE", operations["FENCE"],
        constants={
            "rd": 0,
            "rs1": 0,
        },
        subfields=(
            Field(slice(20, 20), "SW"),
            Field(slice(21, 21), "SR"),
            Field(slice(22, 22), "SO"),
            Field(slice(23, 23), "SI"),
            Field(slice(24, 24), "PW"),
            Field(slice(25, 25), "PR"),
            Field(slice(26, 26), "PO"),
            Field(slice(27, 27), "PI"),
            Field(slice(28, 31), "fm"),
        ),
    ),

    # Environment Call and Breakpoints

    "ECALL": PseudoInstruction("ECALL", operations["SYSTEM"],
        constants={
            "rd": 0,
            "rs1": 0,
            "funct3": 0b000,  # PRIV
            "imm": 0b000,
        },
        subfields=(
            Field(slice(20, 20), "SW"),
            Field(slice(21, 21), "SR"),
            Field(slice(22, 22), "SO"),
            Field(slice(23, 23), "SI"),
            Field(slice(24, 24), "PW"),
            Field(slice(25, 25), "PR"),
            Field(slice(26, 26), "PO"),
            Field(slice(27, 27), "PI"),
            Field(slice(28, 31), "fm"),
        ),
    ),
    "EBREAK": PseudoInstruction("EBREAK", operations["SYSTEM"],
        constants={
            "rd": 0,
            "rs1": 0,
            "funct3": 0b000,  # PRIV
            "imm": 0b000,
        },
        subfields=(
            Field(slice(20, 20), "SW"),
            Field(slice(21, 21), "SR"),
            Field(slice(22, 22), "SO"),
            Field(slice(23, 23), "SI"),
            Field(slice(24, 24), "PW"),
            Field(slice(25, 25), "PR"),
            Field(slice(26, 26), "PO"),
            Field(slice(27, 27), "PI"),
            Field(slice(28, 31), "fm"),
        ),
    ),


}


aliases: Dict[str, PseudoInstruction] = {
    "NOP": PseudoInstruction("ADDI", operations["OP-IMM"], {
        "funct3": 0b000,
        "imm": 0,
    }),
}


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4