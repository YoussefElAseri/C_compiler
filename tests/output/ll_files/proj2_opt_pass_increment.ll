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
; intnumber=-55
%number = alloca i32
store i32 -55, i32* %number
; number++
%1 = load i32, i32* %number
%2 = add i32 %1, 1
; number=number++
%3 = load i32, i32* %number
%4 = add i32 %3, 1
store i32 %4, i32* %number
; intn=number++
%n = alloca i32
%5 = load i32, i32* %number
%6 = add i32 %5, 1
store i32 %6, i32* %n
; n=n-n++
%7 = load i32, i32* %n
%8 = load i32, i32* %n
%9 = add i32 %8, 1
%10 = sub i32 %7, %9
store i32 %10, i32* %n
ret i1 0
}
