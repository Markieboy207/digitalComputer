import warnings
from math import sqrt, floor


class Storage:
    def __init__(self, size):
        self.size = size
        self.memory = [0 for _ in range(size)]
    
    def read(self, address):
        if address < 0 or address >= self.size:
            raise IndexError("Address out of bounds")
        return self.memory[address]
    
    def dual_read(self, address1, address2):
        return self.read(address1), self.read(address2)
    
    def write(self, address, value):
        if address < 0 or address >= self.size:
            raise IndexError("Address out of bounds")
        elif address == 0:
            warnings.warn('Writing to address 0. Any value save to address 0 will not be saved')
        else:
            self.memory[address] = value
    
    def show(self):
        width = floor(sqrt(len(self.memory)))
        for i in range(0, len(self.memory), int(width)):
            print(self.memory[i:min(i+int(width), len(self.memory))])

class Stack:
    def __init__(self, size=256):
        self.stack = []
        self.size = size
    
    def push(self, value):
        self.stack.append(value)
        if len(self.stack) > self.size:
            self.stack.pop(0)
    
    def pop(self):
        if not self.stack:
            return 0
        return self.stack.pop()

class ProgramCounter:
    def __init__(self, max_value=256):
        self.pc = 0
        self.max_value = max_value
    
    def increment(self):
        self.pc += 1
    
    def set(self, value):
        self.pc = value
    
    def get(self):
        return self.pc

class AritmeticLogicUnit:
    def __init__(self, bits=8):
        self.flags = [0, 0] # Carry Flag, Zero Flag
        self.max_value = (1 << bits) - 1
    
    def set_flags(self, result):
        self.flags[0] = 1 if result > self.max_value else 0
        self.flags[1] = 0 if result == 0 else 1

    def add(self, a, b):
        return a + b
    
    def sub(self, a, b):
        return a - b
    
    def xor(self, a, b):
        return a ^ b
    
    def or_op(self, a, b):
        return a | b
    
    def and_op(self, a, b):
        return a & b
    
    def rsh(self, a):
        return a >> 1
    
    def operate(self, alias, a, b):
        if alias == 'ADD':
            value = self.add(a, b)
        elif alias == 'SUB':
            value = self.sub(a, b)
        elif alias == 'XOR':
            value = self.xor(a, b)
        elif alias == 'OR':
            value = self.or_op(a, b)
        elif alias == 'AND':
            value = self.and_op(a, b)
        elif alias == 'RSH':
            value = self.rsh(a)
        else:
            raise ValueError(f"Unknown instruction: {alias}")
        self.set_flags(value)
        return value % self.max_value