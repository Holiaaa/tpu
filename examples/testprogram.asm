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
