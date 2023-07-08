.data
printf_0: .asciiz "Enter the number of prime numbers required\n"
printf_1: .asciiz "First "
printf_2: .asciiz " prime numbers are :\n"
printf_3: .asciiz "2\n"
printf_4: .asciiz "\n"
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

# intn,i=3,count,c;

 ## intn,i=3,count,c
addi $sp, $sp, -4
addi $sp, $sp, -4
li $t0, 3
sw $t0, 4($sp)
addi $sp, $sp, -4
addi $sp, $sp, -4

# printf("Enter the number of prime numbers required\n");

 ## printf("Enter the number of prime numbers required\n")
la $a0, printf_0
jal printf_string


# scanf("%d",&n);

 ## scanf("%d",&n)
jal scanf_int
sw $v0, 16($sp)
li $a0, '\n'
jal printf_char
lw $t0, 16($sp)
li $t1, 1
slt $t0, $t0, $t1
xori $t0, $t0, 1
beqz $t0 DONE_0

# printf("First %d prime numbers are :\n",n);

 ## printf("First %d prime numbers are :\n",n)
la $a0, printf_1
jal printf_string

lw $t0, 16($sp)
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


# printf("2\n");

 ## printf("2\n")
la $a0, printf_3
jal printf_string

j DONE_0

DONE_0: 


# count=2;

 ## count=2
li $t0, 2
sw $t0, 8($sp)
WHILE_0: 
lw $t1, 8($sp)
lw $t2, 16($sp)
slt $t1, $t2, $t1
xori $t1, $t1, 1
beqz $t1  WHILE_DONE_0

# c=2;

 ## c=2
li $t0, 2
sw $t0, 4($sp)
WHILE_1: 
lw $t1, 4($sp)
lw $t2, 12($sp)
li $t3, 1
subu $t2, $t2, $t3
slt $t1, $t2, $t1
xori $t1, $t1, 1
beqz $t1  WHILE_DONE_1
lw $t2, 12($sp)
lw $t3, 4($sp)
div $t2, $t3
mfhi $t2
li $t3, 0
seq $t2, $t2, $t3
beqz $t2 DONE_1

# break;
b WHILE_DONE_1
j DONE_1

DONE_1: 


# c++;

 ## c++
lw $t0, 4($sp)
addiu $t0, $t0, 1
sw $t0, 4($sp)
j WHILE_1
WHILE_DONE_1:
lw $t0, 4($sp)
lw $t1, 12($sp)
seq $t0, $t0, $t1
beqz $t0 DONE_2

# printf("%d\n",i);

 ## printf("%d\n",i)
lw $t0, 12($sp)
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
la $a0, printf_4
jal printf_string


# count++;

 ## count++
lw $t0, 8($sp)
addiu $t0, $t0, 1
sw $t0, 8($sp)
j DONE_2

DONE_2: 


# i++;

 ## i++
lw $t0, 12($sp)
addiu $t0, $t0, 1
sw $t0, 12($sp)
j WHILE_0
WHILE_DONE_0:

# return0;

# End MIPS Program
li $v0, 10
syscall
