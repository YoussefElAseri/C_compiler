declare i32 @printf(i8*, ...)
@intFormat = private constant [4 x i8] c"%d\0A\00"@floatFormat = private constant [4 x i8] c"%f\0A\00"
define void @printInt(i32 %a) {
%p = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8],
[4 x i8]* @intFormat,i32 0, i32 0), i32 %a)
ret void
}

define void @printFloat(float %a) {
%p = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8],
[4 x i8]* @floatFormat,i32 0, i32 0), float %a)
ret void
}

define i1 @"main"()
{
; constintb=-6250
%b = alloca i32
store i32 -6250, i32* %b
; constintx=5
%x = alloca i32
store i32 5, i32* %x
; int*non_const_pointer=&x
%non_const_pointer = alloca i32*
store i32* %x, i32** %non_const_pointer
; *non_const_pointer=36941
%1 = load i32*, i32** %non_const_pointer
store i32 36941, i32* %1
; non_const_pointer=&b
store i32* %b, i32** %non_const_pointer
; charc='x'
%c = alloca i8
store i8 120, i8* %c
; charnl='\n'
%nl = alloca i8
store i8 10, i8* %nl
; char*char_ptr=&c
%char_ptr = alloca i8*
store i8* %c, i8** %char_ptr
; *char_ptr='\t'
%2 = load i8*, i8** %char_ptr
store i8 9, i8* %2
; char_ptr=&nl
store i8* %nl, i8** %char_ptr
ret i1 0
}
