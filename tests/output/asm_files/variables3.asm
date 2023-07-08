.data
printf_0: .asciiz "; "
printf_1: .asciiz "; "
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

# printf("%d; %d; %d",a[0],a[1],a[2]);

 ## printf("%d; %d; %d",a[0],a[1],a[2])
li $t0, 0
li $t2, 3
subu $t0, $t2, $t0
li $t2, 4
mul $t7, $t0, $t2
li $t2, 12
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

li $t1, 1
li $t3, 3
subu $t1, $t3, $t1
li $t3, 4
mul $t7, $t1, $t3
li $t3, 12
addu $t7, $t3, $t7
add $t7 $t7, $sp
lw $t1, ($t7)
move $a0, $t1
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

li $t2, 2
li $t4, 3
subu $t2, $t4, $t2
li $t4, 4
mul $t7, $t2, $t4
li $t4, 12
addu $t7, $t4, $t7
add $t7 $t7, $sp
lw $t2, ($t7)
move $a0, $t2
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
