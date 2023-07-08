.data
.text
# // Should generate warning

.globl main
main: 

# floatx=0.5;

 ## floatx=0.5
addi $sp, $sp, -4
li $t0, 0x3f000000
mtc1 $t0, $f0
s.s $f0, 4($sp)

# inty=x;

 ## inty=x
addi $sp, $sp, -4
l.s $f0, 8($sp)
cvt.w.s $t1, $f0
sw $t1, 4($sp)

# intz=0.5;

 ## intz=0.5
addi $sp, $sp, -4
li $t0, 0x3f000000
mtc1 $t0, $f0
cvt.w.s $t1, $f0
sw $t1, 4($sp)

# return1;
li $t1, 1
move $v0, $t1

# End MIPS Program
move $a0, $v0
li $v0, 17
syscall
