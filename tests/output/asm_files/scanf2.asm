.data
printf_0: .asciiz "Enter a 5-character string:"
scanf_0: .space 100
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

# chara[5];
addi $sp, $sp, -20

# printf("Enter a 5-character string:");

 ## printf("Enter a 5-character string:")
la $a0, printf_0
jal printf_string


# scanf("%5s",&a);

 ## scanf("%5s",&a)
la $a0, scanf_0
li $a1, 6
jal scanf_string

la $t1, scanf_0
lb $t0, 0($t1)
li $t1, 20
add $t1 $t1, $sp
sb $t0, ($t1)

la $t1, scanf_0
lb $t0, 1($t1)
li $t1, 16
add $t1 $t1, $sp
sb $t0, ($t1)

la $t1, scanf_0
lb $t0, 2($t1)
li $t1, 12
add $t1 $t1, $sp
sb $t0, ($t1)

la $t1, scanf_0
lb $t0, 3($t1)
li $t1, 8
add $t1 $t1, $sp
sb $t0, ($t1)

la $t1, scanf_0
lb $t0, 4($t1)
li $t1, 4
add $t1 $t1, $sp
sb $t0, ($t1)
li $a0, '\n'
jal printf_char

# printf("%s",a);

 ## printf("%s",a)
lb $a0, 20($sp)
jal printf_char

lb $a0, 16($sp)
jal printf_char

lb $a0, 12($sp)
jal printf_char

lb $a0, 8($sp)
jal printf_char

lb $a0, 4($sp)
jal printf_char


# return1;
li $t0, 1
move $v0, $t0

# End MIPS Program
move $a0, $v0
li $v0, 17
syscall
