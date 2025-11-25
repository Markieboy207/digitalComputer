from functions import INSTRUCTIONS, SUDO_INSTRUCTIONS

file = open("test.as", "r")
program = file

# (1) remove comments and empty lines
noComments = []
for line in program:
    if len(line.strip()) != 0 and line[0:1] != "//":
        noComments.append(line)
program = noComments

# (2) replace variable names with their respective register/memory addresses
variables = {} # variable: (address, type)
for line in program:
    parts = line.split()
    if parts[0] == "#name":
        variables[parts[2]] = (parts[1][1:], parts[1][0])

noVariables = []
for line in program:
    newLine = []
    for part in line.split():
        if part in variables:
            newLine.append(variables[part][0])
        else:
            newLine.append(part)
    noVariables.append(" ".join(newLine))
program = noVariables

# (3) replace sudo instructions
noSudo = []
for line in program:
    parts = line.split()
    if parts[0] not in SUDO_INSTRUCTIONS:
        noSudo.append(line)
        continue
    
    newLines = SUDO_INSTRUCTIONS[parts[0]].translate(line)
    for newLine in newLines:
        noSudo.append(newLine)
program = noSudo
print(*program)

# (4) replace BRH conditions with integer values
correctedBRH = []
BRHindex = {
    "00": "0",
    "==": "0",
    "0":  "0",
    "01": "1",
    "!=": "1",
    "1":  "1",
    "10": "2",
    ">=": "2",
    "2":  "2",
    "11": "3",
    "<":  "3",
    "3":  "3",
}

for line in program:
    parts = line.split()
    if parts[0] != "BRH":
        correctedBRH.append(line)
        continue
    parts[1] = BRHindex[parts[1]]
    correctedBRH.append(" ".join(parts))
program = correctedBRH

# (5) calculate label indexes
noLabelInit = []
labels = {}
index = 0

for line in program:
    parts = line.split()
    if parts[0] == ".label":
        labels[parts[1]] = index
    else:
        noLabelInit.append(line)
        index += 1

noLabel = []

for line in noLabelInit:
    parts = line.split()
    newLine = [parts[0]]
    for part in parts[1:]:
        if part in labels:
            newLine.append(labels[part])
        else:
            newLine.append(part)
    noLabel.append(" ".join(newLine))

program = noLabel

# (6) assemble
output = open("assembler_output.as", "w")

for line in program:
    parts = line.split()
    if not parts:
        continue
    instr = parts[0]
    operands = parts[1:] if len(parts) > 1 else []
    
    if instr not in INSTRUCTIONS:
        raise ValueError(f"Unknown instruction: {instr}")
    
    instruction = INSTRUCTIONS[instr]
    binary_code = instruction.encode(operands)
    output.write(binary_code + '\n')
    print(f"{binary_code} <- {instr} {' '.join(operands)}")