"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # R0 - R7
        self.ram = [0] * 256 #  256 bites memory
        self.pc = 0
        self.running = True
        self.codes = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b10100011: self.DIV,
            0b10100000: self.ADD,
            0b10100001: self.SUB
        }
    
    
    def ram_read(self, MAR):
        # Accepts the address to read and returns the value stored there
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # Accepts a value to wrie and address to write it to
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a pr ogram:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: cpu.py filename")
            sys.exit(1)
        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue
                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number '{n}'")
                        sys.exit(1)
                        
                    self.ram[address] = n
                    address += 1
        
        except FileNotFoundError:
            print(f"File not Found: {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]
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
    
    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])

    def HLT(self):
        exit()

    def MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
    
    def DIV(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("DIV", operand_a, operand_b)

    def ADD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("ADD", operand_a, operand_b)

    def SUB(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("SUB", operand_a, operand_b)
        
    def run(self):
        """Run the CPU."""

        self.running = True
        
        while self.running:
            ir = self.ram_read(self.pc)
            self.codes[ir]()
            number_of_operands = (ir & 0b11000000) >> 6
            how_far_to_move_pc = number_of_operands + 1
            self.pc += how_far_to_move_pc 

        # if ir == '00000001':
        #     running = false 
        #     pc += 1
        # elif ir == '10000010':
        #     self.reg[operand_a] = 
 
    # def HLT():
    #     exit()

    # def LDI():
    #     self.ram_read