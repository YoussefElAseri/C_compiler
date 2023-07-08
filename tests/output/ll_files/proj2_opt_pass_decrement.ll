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
; intx=5
%x = alloca i32
store i32 5, i32* %x
; x--
%1 = load i32, i32* %x
%2 = sub i32 %1, 1
; intz=x--
%z = alloca i32
%3 = load i32, i32* %x
%4 = sub i32 %3, 1
store i32 %4, i32* %z
; x=x--+z--
%5 = load i32, i32* %x
%6 = sub i32 %5, 1
%7 = load i32, i32* %z
%8 = sub i32 %7, 1
%9 = add i32 %6, %8
store i32 %9, i32* %x
ret i1 0
}
