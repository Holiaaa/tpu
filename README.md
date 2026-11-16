# TPU (Téo Processing Unit)

Custom CPU architecture that comes with :
- The TPU Emulator (`cpu.py`) : Execute program in CLI.
- TPU Assembler (`tasm.py`) : Assemble .asm program into binary.
- Téo CPU Emulator X (`tcex.py`) : GUI application to launch roms and have a better view of what's happening.
- TPU ISA (`cpu_instructions.txt`) : All instructions supported by TPU.

The TPU is also documented in a french technical document : [Here](https://github.com/Holiaaa/tpu/blob/main/docs/TPU-French-Technical.pdf)

Here is a test program that the TPU can run (`examples/testprogram.asm`):
```asm
@INCLUDE "std/math.asm"
@INCLUDE "std/io.asm"

; Test program to check if 8x4 is equal to 32.
; If it's equal, at the end register A should have the value 1.
; If not, the register B will have the value 1.

MOV A 8
MOV B 4

; STD_MUL is a function that multiply regA by regB and store the result in regC.
CALL %STD_MUL

CMP C 32
; STD_RESET is a function that set all registers to 0.
CALL %STD_RESET

JEQ %CORRECT
JNE %INCORRECT

CORRECT:
MOV A 1
; STD_RESETF is a function that set the FLAG to 0.
CALL %STD_RESETF
HLT

INCORRECT:
MOV B 1
CALL %STD_RESETF
HLT
```
- To compile the program run : `python tasm.py examples/testprogram.asm rom.bin`
- To execute it (using TPU Emulator) : `python cpu.py rom.bin`
  
You should have at the end :
```txt
====== TPU 8BIT ======
A: 1
B: 0
C: 0
D: 0
PC: 9
SP: 0x4000
FLAG: 0
```
