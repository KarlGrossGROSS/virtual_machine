import sys

OPS = {
    "hlt": {"code": 0x1, "fmt": "--"},  # Halt program
    "ldc": {"code": 0x2, "fmt": "rv"},  # Load value
    "ldr": {"code": 0x3, "fmt": "rr"},  # Load register
    "cpy": {"code": 0x4, "fmt": "rr"},  # Copy register
    "str": {"code": 0x5, "fmt": "rr"},  # Store register
    "add": {"code": 0x6, "fmt": "rr"},  # Add
    "sub": {"code": 0x7, "fmt": "rr"},  # Subtract
    "beq": {"code": 0x8, "fmt": "rv"},  # Branch if equal
    "bne": {"code": 0x9, "fmt": "rv"},  # Branch if not equal
    "prr": {"code": 0xA, "fmt": "r-"},  # Print register
    "prm": {"code": 0xB, "fmt": "r-"},  # Print memory
}

OP_MASK = 0xFF
OP_SHIFT = 8

class Disassembler:
    def disassemble(self, program):
        assembly_lines = []
        for instruction in program:
            op = instruction & OP_MASK
            instruction >>= OP_SHIFT
            arg0 = instruction & OP_MASK
            instruction >>= OP_SHIFT
            arg1 = instruction & OP_MASK
            assembly_lines.append(self._to_assembly(op, arg0, arg1))
        return assembly_lines

    def _to_assembly(self, op, arg0, arg1):
        for asm_op, info in OPS.items():
            if info['code'] == op:
                return self._format_assembly(asm_op, info['fmt'], arg0, arg1)
        raise ValueError(f"Unknown op code {op}")

    def _format_assembly(self, asm_op, fmt, arg0, arg1):
        if fmt == "--":
            return asm_op
        elif fmt == "r-":
            return f"{asm_op} R{arg0}"
        elif fmt == "rr":
            return f"{asm_op} R{arg0}, R{arg1}"
        elif fmt == "rv":
            return f"{asm_op} R{arg0}, @{arg1:03}"

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.mx output.as")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        program = [int(line.strip(), 16) for line in f if line.strip()]

    disassembler = Disassembler()
    assembly_lines = disassembler.disassemble(program)

    with open(sys.argv[2], 'w') as f:
        for line in assembly_lines:
            print(line, file=f)

if __name__ == "__main__":
    main()
