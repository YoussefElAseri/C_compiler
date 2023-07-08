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
; intx=-60
%x = alloca i32
store i32 -60, i32* %x
; int*some_pointer=&x
%some_pointer = alloca i32*
store i32* %x, i32** %some_pointer
; *some_pointer=53
%1 = load i32*, i32** %some_pointer
store i32 53, i32* %1
; int**another_pointer=&some_pointer
%another_pointer = alloca i32**
store i32** %some_pointer, i32*** %another_pointer
; int***triple_pointer=&another_pointer
%triple_pointer = alloca i32***
store i32*** %another_pointer, i32**** %triple_pointer
; inty=***triple_pointer
%y = alloca i32
%2 = load i32***, i32**** %triple_pointer
%3 = load i32**, i32*** %2
%4 = load i32*, i32** %3
%5 = load i32, i32* %4
store i32 %5, i32* %y
ret i1 0
}
