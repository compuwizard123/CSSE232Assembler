add $t0 $t1 $t2
addi $t0 00000001
test:
mtt $t0 $s0
beq $t0 $s0 00001
jal 00000000001
