from functions import OPERATIONS

file = open("test.as", "r")
output = open("assembler_output.as", "w")

for line in file:
    parts = line.split()
    if not parts:
        continue
    instr = parts[0]
    operands = parts[1:] if len(parts) > 1 else []
    
    if instr not in OPERATIONS:
        raise ValueError(f"Unknown instruction: {instr}")
    
    operation = OPERATIONS[instr]
    binary_code = operation.encode(operands)
    output.write(binary_code + '\n')
    print(f"{binary_code} <- {instr} {' '.join(operands)}")