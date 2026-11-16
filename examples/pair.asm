; Détermine si un nombre est pair ou pas.

@INCLUDE "std/math.asm"

MOV A 92
; La fonction STD_ISPAIR détermine si la valeur du registre A est pair.
; Elle stocke le résultat dans le FLAG (en mettant 1 si pair et 0 si impair)
CALL %STD_ISPAIR
HLT
