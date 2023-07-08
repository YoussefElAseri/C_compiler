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
; intx=6
%x = alloca i32
store i32 6, i32* %x
br label %1

1:
%2 = load i32, i32* %x
%3 = icmp slt i32 %2, 10
br i1 %3, label %4, label %10

4:
; x=x+1
store i32 7, i32* %x
%5 = load i32, i32* %x
%6 = icmp sgt i32 %5, 9
br i1 %6, label %7, label %8

7:
br label %7
br label %8

8:
; printf(x)
%9 = load i32, i32* %x
call void @printInt(i32 %9)
br label %1

10:
; inti=7
%i = alloca i32
store i32 7, i32* %i
ret i1 0
}
