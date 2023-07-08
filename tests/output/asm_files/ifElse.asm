.data
printf_0: .asciiz "Something went wrong"
printf_1: .asciiz "Hello world!\n"
printf_2: .asciiz "Hello world!\n"
printf_3: .asciiz "Something went wrong"
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

# intx=5;

 ## intx=5
addi $sp, $sp, -4
li $t0, 5
sw $t0, 4($sp)
lw $t1, 4($sp)
li $t2, 5
slt $t1, $t1, $t2
beqz $t1 ELSE_0

# printf("Something went wrong");

 ## printf("Something went wrong")
la $a0, printf_0
jal printf_string

# // Should not print

j DONE_0

ELSE_0: 


# printf("Hello world!\n");

 ## printf("Hello world!\n")
la $a0, printf_1
jal printf_string

# // Should print

DONE_0: 

lw $t-1, 4($sp)
li $t0, 5
seq $t-1, $t-1, $t0
li $t0, 1
and $t-1, $t-1, $t0
beqz $t-1 DONE_1
lw $t0, 4($sp)
li $t1, 5
seq $t0, $t0, $t1
beqz $t0 ELSE_2

# printf("Hello world!\n");

 ## printf("Hello world!\n")
la $a0, printf_2
jal printf_string

# // Should print

j DONE_2

ELSE_2: 


# printf("Something went wrong");

 ## printf("Something went wrong")
la $a0, printf_3
jal printf_string

# // Should not print

DONE_2: 

j DONE_1

DONE_1: 


# return1;
li $t-2, 1
move $v0, $t-2

# End MIPS Program
move $a0, $v0
li $v0, 17
syscall
