"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.sp = self.reg[6]
        self.ram = [0] * 256
        self.flag = 0b00000000
        self.running = True
        self.branch_table = {
            0b01000111: self.PRN,
            0b10000010: self.LDI,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b01000110: self.POP,
            0b01000101: self.PUSH,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100111: self.CMP
        }
        
    # new functions for read and write
    def ram_read(self, index): 
        return self.reg[index]

    def ram_write(self, index, value):
        self.reg[index] = value


    # cleaned up while loop to be functions
    def LDI(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.reg[operand_a] = operand_b
        self.pc += 3  

    def PRN(self):
        operand_a = self.ram[self.pc + 1]
        print(self.reg[operand_a])
        self.pc += 2

    def HLT(self):
        self.running = False 

    def MUL(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.alu('MUL', operand_a, operand_b)
        self.pc += 3

    def PUSH(self):
        operand_a = self.ram[self.pc + 1]
        self.sp -= 1
        self.ram[self.sp] = self.reg[operand_a]
        self.pc += 2

    def POP(self):
        operand_a = self.ram[self.pc + 1]
        self.reg[operand_a] = self.ram[self.sp]
        self.sp += 1
        self.pc += 2

    def CALL(self):
        return_address = self.pc + 2
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = return_address
        register = self.ram[self.pc + 1]
        self.pc = self.reg[register]

    def RET(self):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1    

    def CMP(self):
        # This compares the values in the two registers
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.alu('CMP', operand_a, operand_b)
        self.pc += 3



    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: cpu.py filename")
            sys.exit(1)

        try: 
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split('#')
                    code_value = split_line[0].strip()

                    if code_value == "":
                        continue

                    num = int(code_value, 2)
                    self.ram[address] = num
                    address += 1    

        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program was empty!")


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
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                # set the E flag to 1
                self.flag = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                # set the L flag to 1
                self.flag = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                # set the G flag to 1
                self.flag = 0b00000010
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
            instruction = self.ram[self.pc]

            if instruction in self.branch_table:
                self.branch_table[instruction]()

            else:
                print(f"Bad input: {instruction}")
                self.running = False