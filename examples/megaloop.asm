; Valeur de départ
MOV A 4
; Valeur d'arrivé
MOV B 30
; Valeur a incrémenter
MOV C 1

CALL %LOOP
HLT

LOOP:
ADDR A C
CMPR A B
JNE %LOOP
MOV B 0
MOV C 0
RET