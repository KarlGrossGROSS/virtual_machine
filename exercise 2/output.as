ldc R0, @000
ldc R1, @003
prr R0
ldc R2, @001
add R0, R2
cpy R2, R1
sub R2, R0
bne R2, @002
hlt
