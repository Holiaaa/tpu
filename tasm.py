"""
Téo Assembler (TASM)

usage: python tasm.py source.asm output.bin

You can try using files from the examples folder.
"""

import sys

if len(sys.argv) < 3:
    print("usage: python tasm.py source.asm output.bin")
    exit()

input = sys.argv[1]
output = sys.argv[2]

files = [input]

regs = {'A': 10, 'B': 11, 'C': 12, 'D': 13}
output_code = []

labels = {}
ip = 0
oip = 0

code = ""

with open(files[0], "r") as f:
    for line in f.readlines():
        if not line.startswith("@"):
            continue

        splitedline = line.split()
        file = splitedline[1].replace('"', "")
        files.append(file)
    f.close()

for file in files:
    with open(file) as g:
        code += g.read() + "\n"

tmpfile = open(input.split(".")[0] + ".tasmtmp", "w")
tmpfile.write(code)
tmpfile.close()

with open(input.split(".")[0] + ".tasmtmp", "r") as l:
    for j in l:
        line = j.strip()

        if not line or line.startswith(";") or line.startswith("@"):
            continue

        if line.endswith(":"):
            label = line[:-1]
            labels[label] = ip
        else:
            ip += 1
    l.close()

with open(input.split(".")[0] + ".tasmtmp", "r") as f:
    for i in f.readlines():
        if not i.startswith(";") and not i.startswith("\n") and not i.startswith("@"):
            line = i.split()
            if line[0].upper() == "MOV":
                reg = line[1]
                value = line[2]
                output_code += [(0xF << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "ADD":
                reg = line[1]
                value = line[2]
                output_code += [(0xE << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "SUB":
                reg = line[1]
                value = line[2]
                output_code += [(0xD << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "MOVR":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xC0]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "ADDR":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xC1]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "SUBR":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xC2]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "JMP":
                value = line[1]
                if value.startswith("%"):
                    value = labels[value[1:]]
                output_code += [0xC3]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "JEQ":
                value = line[1]
                if value.startswith("%"):
                    value = labels[value[1:]]
                output_code += [0xC4]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "JNE":
                value = line[1]
                if value.startswith("%"):
                    value = labels[value[1:]]
                output_code += [0xC5]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "CMP":
                reg = line[1]
                value = line[2]
                output_code += [(0x9 << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "CGT":
                reg = line[1]
                value = line[2]
                output_code += [(0x8 << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "CLT":
                reg = line[1]
                value = line[2]
                output_code += [(0x7 << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "CGE":
                reg = line[1]
                value = line[2]
                output_code += [(0x6 << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "CLE":
                reg = line[1]
                value = line[2]
                output_code += [(0x5 << 4) + regs[reg]]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "CMPR":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xC6]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "CGTR":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xC7]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "CLTR":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xC8]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "INC":
                reg = line[1]
                output_code += [0xC9]
                output_code += [(regs[reg] << 4)]
                ip += 1
                continue
            elif line[0].upper() == "DEC":
                reg = line[1]
                output_code += [0xCA]
                output_code += [(regs[reg] << 4)]
                ip += 1
                continue
            elif line[0].upper() == "CGER":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xCB]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "CLER":
                reg1 = line[1]
                reg2 = line[2]
                output_code += [0xCC]
                output_code += [(regs[reg1] << 4) + (regs[reg2])]
                ip += 1
                continue
            elif line[0].upper() == "STO":
                value = line[1]
                output_code += [0xB0]
                output_code += [int(value)]
                ip += 1
                continue
            elif line[0].upper() == "LOA":
                reg = line[1]
                output_code += [(0xB << 4) + regs[reg]]
                output_code += [0x00]
                ip += 1
                continue
            elif line[0].upper() == "STOR":
                reg = line[1]
                output_code += [(0xA << 4) + regs[reg]]
                output_code += [0x00]
                ip += 1
                continue
            elif line[0].upper() == "PUSH":
                reg = line[1]
                output_code += [(0x0 << 4) + regs[reg]]
                output_code += [0x00]
                ip += 1
                continue
            elif line[0].upper() == "POP":
                reg = line[1]
                output_code += [(0x1 << 4) + regs[reg]]
                output_code += [0x00]
                ip += 1
                continue
            elif line[0].upper() == "CALL":
                value = line[1]

                if value.startswith("%"):
                    value = labels[value[1:]]

                output_code += [0x2A]
                output_code += [int(value)]
                ip += 1
                continue

            elif line[0].upper() == "RET":
                output_code += [0x2B]
                output_code += [0x00]
                ip += 1
                continue
            elif line[0].upper() == "HLT":
                output_code += [0xFF]
                output_code += [0xFF]
                ip += 1
                continue
    f.close()

with open(output, "wb") as f:
    for opcode in output_code:
        f.write(opcode.to_bytes())
    f.close()
