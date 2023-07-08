.data
printf_0: .asciiz "; "
printf_1: .asciiz "\n"
printf_2: .asciiz "; "
printf_3: .asciiz "\n"
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

# // This should print: 10, 10, 11, 11

.globl main
main: 

# intx=0;

 ## intx=0
addi $sp, $sp, -4
li $t0, 0
sw $t0, 4($sp)

# int*xp=&x;

 ## int*xp=&x
addi $sp, $sp, -4
addi $t0, $sp, 8
sw $t0, 4($sp)

# *xp=10;

 ## *xp=10
lw $t0, 4($sp)
lw $t0, ($t0)
move $t7, $t0
add $t7, $t7, $sp
li $t0, 10
sw $t0, ($t7)

# printf("%d; ",x);

 ## printf("%d; ",x)
lw $t0, 8($sp)
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


# printf("%d\n",*xp);

 ## printf("%d\n",*xp)
lw $t0, 4($sp)
lw $t0, ($t0)
move $t7, $t0
add $t7, $t7, $sp
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
la $a0, printf_1
jal printf_string


# (*xp)++;

 ## (*xp)++
lw $t0, 4($sp)
lw $t0, ($t0)
move $t7, $t0
add $t7, $t7, $sp
addiu $t0, $t0, 1
sw $t0, ($t7)

# printf("%d; ",x);

 ## printf("%d; ",x)
lw $t0, 8($sp)
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
la $a0, printf_2
jal printf_string


# printf("%d\n",*xp);

 ## printf("%d\n",*xp)
lw $t0, 4($sp)
lw $t0, ($t0)
move $t7, $t0
add $t7, $t7, $sp
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
la $a0, printf_3
jal printf_string


# return1;
li $t0, 1
move $v0, $t0

# End MIPS Program
move $a0, $v0
li $v0, 17
syscall
