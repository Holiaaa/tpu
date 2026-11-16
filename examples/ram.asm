; This program store 10 into ram at adress : 0x0001
; And reads the same adresse to store the result into B

MOV A 10
MOV C 0
MOV D 1
STOR A

LOA B
HLT