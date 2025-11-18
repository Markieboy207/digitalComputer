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

class Operation:
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
            raise ValueError("Opcode does not match this operation")
        
        operands = []
        index = 0
        
        for segment, size in zip(self.segments, self.sizes):
            operand_binary = operands_binary[index:index+size]
            index += size
            
            if segment == 'None':
                continue
            else:
                operand_value = BTD(operand_binary)
                operands.append(operand_value)
        
        return operands

OPERATIONS = {  
    'HLT': Operation(opcode=0),
    'LDI': Operation(opcode=1, segments=['REG A', 'VALUE'], sizes=[4, 8]),
    'CAL': Operation(opcode=2, segments=['REG A', 'MEM B'], sizes=[4, 8]),
    'STR': Operation(opcode=3, segments=['REG A', 'MEM B'], sizes=[4, 8]),
    'JMP': Operation(opcode=4, segments=['None', 'ADDRESS'], sizes=[2, 10]),
    'BRH': Operation(opcode=5, segments=['Flags', 'ADDRESS'], sizes=[2, 10]),
    'PSH': Operation(opcode=6),
    'RET': Operation(opcode=7),
    'ADD': Operation(opcode=8, segments=['REG A', 'REG B', 'REG C'], sizes=[4, 4, 4]),
    'SUB': Operation(opcode=9, segments=['REG A', 'REG B', 'REG C'], sizes=[4, 4, 4]),
    'XOR': Operation(opcode=10, segments=['REG A', 'REG B', 'REG C'], sizes=[4, 4, 4]),
    'OR': Operation(opcode=11, segments=['REG A', 'REG B', 'REG C'], sizes=[4, 4, 4]),
    'AND': Operation(opcode=12, segments=['REG A', 'REG B', 'REG C'], sizes=[4, 4, 4]),
    'RSH': Operation(opcode=13, segments=['REG A', 'None', 'REG C'], sizes=[4, 4, 4])
}