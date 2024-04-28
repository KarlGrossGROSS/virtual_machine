# Count up to 3.
# - R0: loop index.
# - R1: loop limit.
# - R2: array index.
# - R3: temporary.
ldc R0 0
ldc R1 7
ldc R2 @array
loop:
str R0 R2
ldc R3 1 
add R0 R3
add R2 R3
cpy R3 R1
sub R3 R0
bne R3 @loop

dec R1
ldc R2 @array
ldc R3 @array
add R3 R1
loop1:
ldr R0 R2
ldr R1 R3
str R0 R3
str R1 R2
inc R2
dec R3
cpy R0 R2
cpy R1 R3
sub R1 R0
bt0 R1 @loop1

hlt
.data
array: 10