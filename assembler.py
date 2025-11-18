def DTB(decimal_value, length):
    if decimal_value == 0:
        return "0"*length
    binary_value = ""
    while decimal_value > 0:
        binary_value = str(decimal_value % 2) + binary_value
        decimal_value //= 2
    return binary_value.zfill(length)

class Operation:
    def __init__(self, opcode, segments=None, sizes=None):
        self.opcode = DTB(opcode, 4)
        self.segments = segments if segments is not None else []
        self.sizes = sizes if sizes is not None else []
    
    def encode(self, operands):
        if len(operands) != len(self.segments) - self.segments.count('None'):
            raise ValueError(f"Expected {len(self.segments) - self.segments.count('None')} operands, got {len(operands)}")
        
        binary_instruction = ''
        
        for operand, size in zip(operands, self.sizes):
            if size == 'None':
                binary_instruction += '0' * size
            else:
                binary_instruction += DTB(int(operand), size)

        return self.opcode + binary_instruction.zfill(12)
    
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