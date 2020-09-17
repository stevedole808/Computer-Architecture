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
        self.SP = 7
        self.reg[self.SP] = 0xF4
    
    
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

    def MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

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

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        reg_num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[reg_num] = value
        self.reg[operand_a] = operand_b
        self.pc += 3

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += 2

    def HLT(self):
        exit()
    
    def push_value(self, value):
        self.reg[self.SP] -= 1
        top_of_stack_order = self.reg[self.SP]
        self.ram[top_of_stack_order] = value
    
    def pop_value(self):
        # Pop the value at the top of the stack into the given register
        top_of_stack_order = self.reg[self.SP]
        value = self.ram[top_of_stack_order]
        self.reg[self.SP] += 1
        return value

    def PUSH(self):
        # Get the reg num to push
        reg_num = self.ram[self.pc + 1]
        # Get the value to push
        value = self.reg[reg_num]
        # Copy the value to the Stack Pointer address
        self.push_value(value)
        self.pc += 2

    def POP(self):
        reg_num = self.ram[self.pc + 1]
        value = self.pop_value()
        self.reg[reg_num] = value
        self.pc += 2

    def CALL(self):
        # compute the return addr
        return_addr = self.pc + 2
        print(return_addr)
        sys.exit(3)
        # Push return addr on stack
        self.push_value(return_addr) 
        # Get the value from the operand reg
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        # Set the pc to the value
        self.pc = value
    
    def RET(self):
        pass

    def run(self):
        """Run the CPU."""

        self.running = True
            
        while self.running:
            LDI = 0b10000010
            PRN = 0b01000111
            HLT = 0b00000001
            CALL = 0b01010000
            PUSH = 0b01000101
            POP = 0b01000110
            RET = 0b00010001
            MUL = 0b10100010
            DIV = 0b10100011
            ADD = 0b10100000
            SUB = 0b10100001

            ir = self.ram_read(self.pc)

            if ir == LDI:
                self.LDI()
            elif ir == PRN:
                self.PRN()
            elif ir == HLT:
                self.HLT()
            elif ir == PUSH:
                self.PUSH()
            elif ir == POP:
                self.POP()
            elif ir == CALL:
                self.CALL()
            elif ir == RET:
                self.RET()
            elif ir == MUL:
                self.MUL()
            elif ir == ADD:
                self.ADD()
            elif ir == SUB:
                self.SUB()
            elif ir == DIV:
                self.DIV()
            else:
                print(f"Unknown instruction {ir}")
            # self.codes[ir]()
            # inst_sets_pc = (ir >> 4) & 1 == 1
            # if not inst_sets_pc:
            #     number_of_operands = (ir & 0b11000000) >> 6
            #     how_far_to_move_pc = number_of_operands + 1
            #     self.pc += how_far_to_move_pc 
            # else: 
            #     print(f"Uknown instruction {ir}")
