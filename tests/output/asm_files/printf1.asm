.data
printf_0: .asciiz "Hello World!\n"
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

# printf("Hello World!\n");

 ## printf("Hello World!\n")
la $a0, printf_0
jal printf_string

