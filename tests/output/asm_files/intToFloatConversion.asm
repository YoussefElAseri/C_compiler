.data
.text
# // Should NOT generate warning

.globl main
main: 

# intx=5;

 ## intx=5
addi $sp, $sp, -4
li $t0, 5
sw $t0, 4($sp)

# floaty=x;

 ## floaty=x
addi $sp, $sp, -4
lw $t0, 8($sp)
cvt.s.w $f0, $t0
s.s $f0, 4($sp)

# floatz=0.5+1;

 ## floatz=0.5+1
addi $sp, $sp, -4
li $t0, 0x3fc00000
mtc1 $t0, $f0
s.s $f0, 4($sp)

# return1;
li $t0, 1
move $v0, $t0

# End MIPS Program
move $a0, $v0
li $v0, 17
syscall
