def DTB(decimal_value, length):
    if decimal_value == 0:
        return "0"*length
    binary_value = ""
    while decimal_value > 0:
        binary_value = str(decimal_value % 2) + binary_value
        decimal_value //= 2
    return binary_value.zfill(length)

def BTD(binary_string):
    decimal_value = 0
    for index, digit in enumerate(reversed(binary_string)):
        decimal_value += int(digit) * (2 ** index)
    return decimal_value

class Instruction:
    def __init__(self, opcode, segments=None, sizes=None):
        self.opcode = DTB(opcode, 4)
        self.segments = segments if segments is not None else []
        self.sizes = sizes if sizes is not None else []
    
    def encode(self, operands):
        if len(operands) != len(self.segments) - self.segments.count('None'):
            raise ValueError(f"Expected {len(self.segments) - self.segments.count('None')} operands, got {len(operands)}")
        
        if self.segments.count('None') > 0:
            full_operands = []
            operand_index = 0
            for segment in self.segments:
                if segment == 'None':
                    full_operands.append('None')
                else:
                    full_operands.append(operands[operand_index])
                    operand_index += 1
            operands = full_operands

        binary_instruction = ''
        
        for operand, size in zip(operands, self.sizes):
            if operand == 'None':
                binary_instruction += '0' * size
            else:
                binary_instruction += DTB(int(operand), size)

        return self.opcode + binary_instruction.zfill(12)
    
    def decode(self, binary_instruction):
        if len(binary_instruction) != 16:
            raise ValueError("Binary instruction must be 16 bits long")
        
        opcode = binary_instruction[:4]
        operands_binary = binary_instruction[4:]
        
        if opcode != self.opcode:
            raise ValueError("Opcode does not match this instruction")
        
        operands = []
        index = 0
        
        for segment, size in zip(self.segments, self.sizes):
            operand_binary = operands_binary[index:index+size]
            index += size
            
            if segment == 'none':
                continue
            else:
                operand_value = BTD(operand_binary)
                operands.append(operand_value)
        
        return operands

class SudoInstruction:
    # input:  "INSTRUCTION type type type"
    # output: ["INSTRUCTION type type type", "INSTRUCTION type type type"]
    # types: regA-regO, addr
    #        memA-memZ, none
    #        flag, reg0, valu
    # example:
    # input: "CMP regA regB"
    # output: ["SUB regA regB 0"]

    def __init__(self, sudo=None, instruction=[]):
        self.sudo = sudo if sudo != None else ""
        self.instruction = instruction

        self.sudoOperands = self.sudo.split()[1:]

    def translate(self, operands):
        corrected = []
        for instruct in self.instruction:
            line = []
            for operand in instruct.split():
                if self.sudoOperands.count(operand) != 0:
                    line.append(operands[self.sudoOperands.index(operand)])
                else:
                    line.append(operand)
            corrected.append(" ".join(line))
        return corrected

INSTRUCTIONS = {  
    'HLT': Instruction(opcode=0),
    'LDI': Instruction(opcode=1, segments= ['regA', 'valu'], sizes=[4, 8]),
    'CAL': Instruction(opcode=2, segments= ['regA', 'memB'], sizes=[4, 8]),
    'STR': Instruction(opcode=3, segments= ['regA', 'memB'], sizes=[4, 8]),
    'JMP': Instruction(opcode=4, segments= ['none', 'addr'], sizes=[2, 10]),
    'BRH': Instruction(opcode=5, segments= ['flag', 'addr'], sizes=[2, 10]),
    'PSH': Instruction(opcode=6),
    'RET': Instruction(opcode=7),
    'ADD': Instruction(opcode=8, segments= ['regA', 'regB', 'regC'], sizes=[4, 4, 4]),
    'SUB': Instruction(opcode=9, segments= ['regA', 'regB', 'regC'], sizes=[4, 4, 4]),
    'XOR': Instruction(opcode=10, segments=['regA', 'regB', 'regC'], sizes=[4, 4, 4]),
    'OR':  Instruction(opcode=11, segments=['regA', 'regB', 'regC'], sizes=[4, 4, 4]),
    'AND': Instruction(opcode=12, segments=['regA', 'regB', 'regC'], sizes=[4, 4, 4]),
    'RSH': Instruction(opcode=13, segments=['regA', 'none', 'regC'], sizes=[4, 4, 4])
}


SUDO_INSTRUCTIONS = {
    "CMP": SudoInstruction(sudo="CMP regA regB", instruction=["SUB regA regB reg0"])
}