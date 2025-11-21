from functions import INSTRUCTIONS, BTD
from components import *
import json

CONFIG_FILE = open("interpreter_config.json")
CONFIG = json.load(CONFIG_FILE)
print(CONFIG)

aliases = ['HLT','LDI','CAL','STR','JMP','BRH','PSH','RET','ADD','SUB','XOR','OR','AND','RSH']

REG = Storage(CONFIG["RAM_ADDRESSES"])
MEM = Storage(CONFIG["MEMORY_ADDRESSES"])
STACK = Stack(CONFIG["STACK_SIZE"])
PC = ProgramCounter(CONFIG["PROGRAM_FILE_SIZE"])
ALU = AritmeticLogicUnit(2 ** CONFIG["INTEGER_BITS"])

file = open("assembler_output.as", "r")

for line in file:
    alias = aliases[BTD(line[:4])]
    instruction = INSTRUCTIONS[alias]
    operands = instruction.decode(line.strip())
    match alias:
        case 'HLT':
            print("Halting execution.")
            break
        case 'LDI':
            REG.write(operands[0], operands[1])
        case 'CAL':
            value = MEM.read(operands[1])
            REG.write(operands[0], value)
        case 'STR':
            value = REG.read(operands[0])
            MEM.write(operands[1], value)
        case 'JMP':
            PC.set(operands[0])
        case 'BRH':
            if operands[0] == ''.join(str(i) for i in ALU.flags):
                PC.set(operands[1])
        case 'PSH':
            value = PC.get()  # Assuming we push the current program counter value
            STACK.push(value)
        case 'RET':
            value = STACK.pop()
            PC.set(value)
        case 'ADD' | 'SUB' | 'XOR' | 'OR' | 'AND' | 'RSH':
            a = REG.read(operands[0])
            b = REG.read(operands[1]) if alias != 'RSH' else 0
            result = ALU.operate(alias, a, b)
            REG.write(operands[2] if alias != 'RSH' else operands[1], result)

REG.show()