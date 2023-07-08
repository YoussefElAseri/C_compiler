.data
printf_0: .asciiz "\n"
.text
printf_string: # Print A String
li $v0, 4
syscall
jr $ra

printf_char: # Print A Char
li $v0, 11
syscall
jr $ra

printf_int: # Print An Integer
li $v0, 1
syscall
jr $ra

printf_float: # Print A Float
li $v0, 2
syscall
jr $ra

scanf_string:
li $v0, 8
syscall
jr $ra

scanf_char:
li $v0, 12
syscall
jr $ra

scanf_int:
li $v0, 5
syscall
jr $ra

.globl main
main: 
# // this should print the numbers: 0, 1, 2, 3, 4, 5


# // this should print the numbers: 0, 1, 2, 3, 4, 5
# inti=0;

 ## inti=0
addi $sp, $sp, -4
li $t0, 0
sw $t0, 4($sp)
WHILE_0: 
lw $t1, 4($sp)
li $t2, 10
slt $t1, $t1, $t2
beqz $t1  WHILE_DONE_0

# printf("%d\n",i);

 ## printf("%d\n",i)
lw $t0, 4($sp)
move $a0, $t0
sw $ra, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
s.s $f0, 0($sp)
addi $sp, $sp, -4
s.s $f1, 0($sp)
addi $sp, $sp, -4
s.s $f2, 0($sp)
addi $sp, $sp, -4
s.s $f3, 0($sp)
addi $sp, $sp, -4
sw $fp, 0($sp)
addi $sp, $sp, -4
addi $fp ,$sp, 0
jal printf_int
addi $sp ,$fp, 0
addi $sp, $sp, 4
lw $fp, 0($sp)
addi $sp, $sp, 4
l.s $f3, 0($sp)
addi $sp, $sp, 4
l.s $f2, 0($sp)
addi $sp, $sp, 4
l.s $f1, 0($sp)
addi $sp, $sp, 4
l.s $f0, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $ra, 0($sp)
la $a0, printf_0
jal printf_string

lw $t1, 4($sp)
li $t2, 5
seq $t1, $t1, $t2
beqz $t1 ELSE_0

# break;
b WHILE_DONE_0
j DONE_0

ELSE_0: 


# i++;

 ## i++
lw $t0, 4($sp)
addiu $t0, $t0, 1
sw $t0, 4($sp)

# continue;
b WHILE_0
DONE_0: 


# i=10;

 ## i=10
li $t0, 10
sw $t0, 4($sp)
j WHILE_0
WHILE_DONE_0:

# return0;

# End MIPS Program
li $v0, 10
syscall
