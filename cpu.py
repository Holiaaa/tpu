"""
TPU Emulator made in Python

usage: python cpu.py rom.bin [--args]

Arguments:
    --showreg       : Show registers each clock tick.
    --sethz=[INT]   : Set Hz frequency of the CPU.
    --setram=[INT]  : Set RAM capacity (in kilobytes) of the CPU.
"""

import time
import sys

__CPU = "TPU"
__VERSION = "1.0"

state = True

class RAM:
    def __init__(self, memory):
        self.memory = memory
        self.ram = [0]*(memory*1024)

class Clock:
    def __init__(self):
        self.hz = 1
        self.time = 1/self.hz

    def set_hertz(self, hertz):
        self.hz = hertz
        self.time = 1/self.hz

class CPU:
    def __init__(self):
        self.reg = [0, 0, 0, 0] # A, B, C, D

        self.pc = 0
        self.sp = 0
        self.flag = 0

        self.rom = [0x00]*2048
        self.ram = []

    def load_rom(self, rom):
        if len(rom) < 2048:
            i = 2048 - len(rom)
            self.rom = rom + i*[0]

    def execute(self):
        global state
        # MOV REG, VALUE -> 0xFRVV
        if (self.rom[self.pc] >> 12) == 0xF and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            value = (self.rom[self.pc] & 0xFF)
            self.reg[reg] = value 
        # ADD REG, VALUE -> 0xERVV
        elif (self.rom[self.pc] >> 12) == 0xE and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            value = (self.rom[self.pc] & 0xFF)
            self.reg[reg] += value 
        # SUB REG, VALUE -> 0xDRVV
        elif (self.rom[self.pc] >> 12) == 0xD and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            value = (self.rom[self.pc] & 0xFF)
            self.reg[reg] -= value 
        # MOVR REG, REG -> 0xC0RR
        elif (self.rom[self.pc] >> 8) == 0xC0:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            self.reg[reg1] = self.reg[reg2]
        # ADDR REG, REG -> 0xC1RR
        elif (self.rom[self.pc] >> 8) == 0xC1:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            self.reg[reg1] += self.reg[reg2]
        # SUBR REG, REG -> 0xC2RR
        elif (self.rom[self.pc] >> 8) == 0xC2:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            self.reg[reg1] -= self.reg[reg2]
        # JMP VALUE -> 0xC3VV
        elif (self.rom[self.pc] >> 8) == 0xC3:
            value = (self.rom[self.pc] & 0xFF)-1
            self.pc = value
        # JEQ VALUE -> 0xC4VV
        elif (self.rom[self.pc] >> 8) == 0xC4:
            value = (self.rom[self.pc] & 0xFF)-1
            if self.flag:
                self.pc = value
        # JNE VALUE -> 0xC5VV
        elif (self.rom[self.pc] >> 8) == 0xC5:
            value = (self.rom[self.pc] & 0xFF)-1
            if not self.flag:
                self.pc = value
        # CMP REG, VALUE -> 0x9RVV
        elif (self.rom[self.pc] >> 12) == 0x9 and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            if (self.rom[self.pc] & 0xFF) == self.reg[reg]:
                self.flag = 1
            else:
                self.flag = 0
        # CGT REG, VALUE -> 0x8RVV
        elif (self.rom[self.pc] >> 12) == 0x8 and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            if (self.rom[self.pc] & 0xFF) < self.reg[reg]:
                self.flag = 1
            else:
                self.flag = 0
        # CLT REG, VALUE -> 0x7RVV
        elif (self.rom[self.pc] >> 12) == 0x7 and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            if (self.rom[self.pc] & 0xFF) > self.reg[reg]:
                self.flag = 1
            else:
                self.flag = 0
        # CGE REG, VALUE -> 0x6RVV
        elif (self.rom[self.pc] >> 12) == 0x6 and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            if (self.rom[self.pc] & 0xFF) <= self.reg[reg]:
                self.flag = 1
            else:
                self.flag = 0
        # CLE REG, VALUE -> 0x5RVV
        elif (self.rom[self.pc] >> 12) == 0x5 and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            if (self.rom[self.pc] & 0xFF) >= self.reg[reg]:
                self.flag = 1
            else:
                self.flag = 0
        # CMPR REG, REG -> 0xC6RR 
        elif (self.rom[self.pc] >> 8) == 0xC6:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            if self.reg[reg1] == self.reg[reg2]:
                self.flag = 1
            else:
                self.flag = 0
        # CGTR REG, REG -> 0xC6RR 
        elif (self.rom[self.pc] >> 8) == 0xC7:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            if self.reg[reg1] > self.reg[reg2]:
                self.flag = 1
            else:
                self.flag = 0
        # CLTR REG, REG -> 0xC6RR 
        elif (self.rom[self.pc] >> 8) == 0xC8:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            if self.reg[reg1] < self.reg[reg2]:
                self.flag = 1
            else:
                self.flag = 0
        # INC REG -> 0xC9R0
        elif (self.rom[self.pc] >> 8) == 0xC9:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            self.reg[reg1] += 1
        # DEC REG -> 0xCAR0
        elif (self.rom[self.pc] >> 8) == 0xCA:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            self.reg[reg1] -= 1
            print("DEC")
        # CGER REG, REG -> 0xCBRR
        elif (self.rom[self.pc] >> 8) == 0xCB:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            if self.reg[reg1] >= self.reg[reg2]:
                self.flag = 1
            else:
                self.flag = 0
        # CLER REG, REG -> 0xCCRR
        elif (self.rom[self.pc] >> 8) == 0xCC:
            reg1 = ((self.rom[self.pc] & 0xFF) >> 4) % 10
            reg2 = ((self.rom[self.pc] & 0xFF) & 0xF) % 10
            if self.reg[reg1] <= self.reg[reg2]:
                self.flag = 1
            else:
                self.flag = 0
        # STO VALUE -> 0xB0VV
        elif (self.rom[self.pc] >> 8) == 0xB0:
            value = (self.rom[self.pc] & 0xFF)
            reg1 = self.reg[2]
            reg2 = self.reg[3]
            self.ram[(reg1 << 8) + reg2] = value
        # LOA REG -> 0xBR00
        elif (self.rom[self.pc] >> 12) == 0xB and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg1 = self.reg[2]
            reg2 = self.reg[3]
            value = self.ram[(reg1 << 8) + reg2]
            self.reg[((self.rom[self.pc] >> 8) & 0xF) % 10] = value
        # STOR REG -> 0xAR00
        elif (self.rom[self.pc] >> 12) == 0xA and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg1 = self.reg[2]
            reg2 = self.reg[3]
            value = self.reg[((self.rom[self.pc] >> 8) & 0xF) % 10]
            self.ram[(reg1 << 8) + reg2] = value
        # PUSH REG -> 0x0R00
        elif (self.rom[self.pc] >> 12) == 0x0 and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            value = self.reg[reg]
            self.sp -= 1
            self.ram[self.sp] = value
        # POP REG -> 0x1R00
        elif (self.rom[self.pc] >> 12) == 0x1 and 10 <= ((self.rom[self.pc] >> 8) & 0xF) <= 13:
            reg = ((self.rom[self.pc] >> 8) & 0xF) % 10
            value = self.ram[self.sp]
            self.reg[reg] = value
            self.ram[self.sp] = 0
            self.sp += 1
        # CALL VALUE -> 0x2AVV
        elif (self.rom[self.pc] >> 8) == 0x2A:
            value = self.rom[self.pc] & 0xFF
            self.sp -= 1
            self.ram[self.sp] = self.pc + 1
            self.pc = value
            return
        # RET -> 0x2B00
        elif (self.rom[self.pc] >> 8) == 0x2B:
            self.pc = self.ram[self.sp]
            self.ram[self.sp] = 0
            self.sp += 1
            return
        # HLT
        elif (self.rom[self.pc] >> 8) == 0xFF:
            state = False
            return
            
        self.pc += 1

        if self.pc > 2047:
            state = False

        for v in self.rom:
            if v < 0:
                state = False
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python cpu.py rom.bin")
        exit()

    SHOW_REGISTERS = False
    HZ = None
    RAMS = None

    if len(sys.argv) > 2:
        for arg in sys.argv:
            if arg == "--showreg":
                SHOW_REGISTERS = True

            if arg.startswith("--sethz="):
                line = arg.split("=")
                HZ = int(line[1])

            if arg.startswith("--setram="):
                line = arg.split("=")
                RAMS = int(line[1])

    cpu = CPU()
    rom = []
    with open(sys.argv[1], "rb") as f:
        while instruction := f.read(2):
            rom.append(int.from_bytes(instruction, byteorder="big"))

    cpu.load_rom(rom)

    if RAMS:
        ram = RAM(RAMS)
    else:
        ram = RAM(16) # en Kilobyte

    cpu.ram = ram.ram
    cpu.sp = len(cpu.ram)

    clock = Clock()

    if HZ:
        clock.set_hertz(HZ)
    else:
        clock.set_hertz(90)

    prochain = time.perf_counter()
    while state:
        cpu.execute()

        if SHOW_REGISTERS:
            print(cpu.reg)

        prochain += clock.time
        pause = prochain - time.perf_counter()
        if pause > 0:
            time.sleep(pause)
        else:
            prochain = time.perf_counter()

    print("====== TPU 8BIT ======")
    print("A:", cpu.reg[0])
    print("B:", cpu.reg[1])
    print("C:", cpu.reg[2])
    print("D:", cpu.reg[3])
    print("PC:", cpu.pc)
    print("SP:", hex(cpu.sp))
    print("FLAG:", cpu.flag)