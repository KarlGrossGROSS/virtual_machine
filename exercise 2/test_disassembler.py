import pytest
from disassembler import Disassembler

# Test with provided input and output
def test_disassembler():
    input_data = [0x000002, 0x030102, 0x00000a, 0x010202, 0x020006, 0x010204, 0x000207, 0x020209, 0x000001]

    expected_output = [
        "ldc R0, @000",
        "ldc R1, @003",
        "prr R0",
        "ldc R2, @001",
        "add R0, R2",
        "cpy R2, R1",
        "sub R2, R0",
        "bne R2, @002",
        "hlt"
    ]

    disassembler = Disassembler()

    actual_output = disassembler.disassemble(input_data)

    assert actual_output == expected_output, "Disassembler output does not match expected output."

# Test with a single instruction
def test_disassembler_single_instruction():
    input_data = [0x000002]  # A single instruction
    expected_output = ["ldc R0, @000"]
    disassembler = Disassembler()
    assert disassembler.disassemble(input_data) == expected_output

# Test with an invalid opcode
def test_disassembler_invalid_opcode():
    input_data = [0x00FFFF]  # Invalid opcode
    disassembler = Disassembler()
    with pytest.raises(ValueError, match="Unknown op code"):
        disassembler.disassemble(input_data)

# Test with no instructions (empty input)
def test_disassembler_empty_input():
    input_data = []
    expected_output = []
    disassembler = Disassembler()
    assert disassembler.disassemble(input_data) == expected_output

def test_hlt_instruction():
    disassembler = Disassembler()
    program = [0x000001] 
    expected_output = ["hlt"]
    print(disassembler.disassemble(program))
    assert disassembler.disassemble(program) == expected_output

def test_ldc_instruction():
    disassembler = Disassembler()
    program = [0x020003]
    expected_output = ["ldr R0, R2"]
    assert disassembler.disassemble(program) == expected_output

def test_add_instruction():
    disassembler = Disassembler()
    program = [0x060102]
    expected_output = ["ldc R1, @006"]
    assert disassembler.disassemble(program) == expected_output



