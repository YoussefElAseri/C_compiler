.data
printf_0: .asciiz "; "
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

# // Should print the numbers 10 20 30

.globl main
main: 

# inta[3];
addi $sp, $sp, -12

# a[0]=10;

 ## a[0]=10
li $t0, 0
li $t2, 3
subu $t0, $t2, $t0
li $t2, 4
mul $t7, $t0, $t2
li $t2, 12
addu $t7, $t2, $t7
add $t7 $t7, $sp
lw $t0, ($t7)
li $t1, 10
sw $t1, ($t7)

# a[1]=20;

 ## a[1]=20
li $t0, 1
li $t2, 3
subu $t0, $t2, $t0
li $t2, 4
mul $t7, $t0, $t2
li $t2, 12
addu $t7, $t2, $t7
add $t7 $t7, $sp
lw $t0, ($t7)
li $t1, 20
sw $t1, ($t7)

# a[2]=30;

 ## a[2]=30
li $t0, 2
li $t2, 3
subu $t0, $t2, $t0
li $t2, 4
mul $t7, $t0, $t2
li $t2, 12
addu $t7, $t2, $t7
add $t7 $t7, $sp
lw $t0, ($t7)
li $t1, 30
sw $t1, ($t7)

# inti=1;

 ## inti=1
addi $sp, $sp, -4
li $t0, 1
sw $t0, 4($sp)
WHILE_0: 
lw $t1, 4($sp)
li $t2, 4
slt $t1, $t1, $t2
beqz $t1  WHILE_DONE_0

# printf("%d; ",a[i-1]);

 ## printf("%d; ",a[i-1])
lw $t0, 4($sp)
li $t1, 1
subu $t0, $t0, $t1
li $t2, 3
subu $t0, $t2, $t0
li $t2, 4
mul $t7, $t0, $t2
li $t2, 16
addu $t7, $t2, $t7
add $t7 $t7, $sp
lw $t0, ($t7)
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


# i++;

 ## i++
lw $t0, 4($sp)
addiu $t0, $t0, 1
sw $t0, 4($sp)
j WHILE_0
WHILE_DONE_0:

# return1;
li $t0, 1
move $v0, $t0

# End MIPS Program
move $a0, $v0
li $v0, 17
syscall
