from functions import OPERATIONS, BTD
from components import *

file = open("assembler_output.as", "r")

aliases = ['HLT','LDI','CAL','STR','JMP','BRH','PSH','RET','ADD','SUB','XOR','OR','AND','RSH']

REG = Storage(16)
MEM = Storage(256)
STACK = Stack(8)
PC = ProgramCounter(1024)
ALU = AritmeticLogicUnit(255)

for line in file:
    alias = aliases[BTD(line[:4])]
    operation = OPERATIONS[alias]
    operands = operation.decode(line.strip())
    
    if alias == 'HLT':
        print("Halting execution.")
        break
    elif alias == 'LDI':
        REG.write(operands[0], operands[1])
    elif alias == 'CAL':
        value = MEM.read(operands[1])
        REG.write(operands[0], value)
    elif alias == 'STR':
        value = REG.get(operands[0])
        MEM.write(operands[1], value)
    elif alias == 'JMP':
        PC.set(operands[0])
    elif alias == 'BRH':
        if operands[0] == ''.join(ALU.flags):
            PC.set(operands[1])
    elif alias == 'PSH':
        value = PC.get()  # Assuming we push the current program counter value
        STACK.push(value)
    elif alias == 'RET':
        value = STACK.pop()
        PC.set(value)
    elif alias in ['ADD', 'SUB', 'XOR', 'OR', 'AND', 'RSH']:
        a = REG.read(operands[0])
        b = REG.read(operands[1]) if alias != 'RSH' else 0
        result = ALU.operate(alias, a, b)
        REG.write(operands[2] if alias != 'RSH' else operands[1], result)

REG.show()