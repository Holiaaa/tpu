; Démonstration des labels de TASM

MOV A 0
LOOP:
INC A
CMP A 10
JNE %LOOP
MOV B 1
HLT
