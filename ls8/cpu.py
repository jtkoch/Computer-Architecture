"""CPU functionality."""

import sys

# filename = "Computer-Architecture/ls8/examples/mult.ls8"

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.running = True

    if len(sys.argv) != 2:
        print("usage: comp.py filename")
        sys.exit(1)

    def load(self):
        """Load a program into memory."""

        address = 0

        try: 
            with open(filename) as f:
                for line in f:
                    split_line = line.spit('#')
                    code_value = split_line[0].strip()

                    if code_value == "":
                        continue

                    num = int(code_value)
                    self.ram[address] = num
                    address += 1    

        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program was empty!")

    # new functions for read and write
    def ram_read(self, index): 
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.running = False
                self.pc += 1

            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == MUL:
                print(self.reg[operand_a] * self.reg[operand_b])
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            else:
                self.running = False
                print(f"Bad input: {instruction}")
