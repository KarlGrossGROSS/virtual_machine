ldc R0 2
ldc R1 3
add R1 R0
ldr R2 R1
cpy R3 R1
sub R2 R0
str R3 R0
prr R0
beq R2 10
bne R0 11
prm R3
hlt