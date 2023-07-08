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
; intx=54;
%x = alloca i32
store i32 54, i32* %x
; intz=-33;
%z = alloca i32
store i32 -33, i32* %z
; int*p=&z;
%p = alloca i32*
store i32* %z, i32** %p
; p=*x;
%1 = load i32, i32* %x
store i32 %1, i32** %p
ret i1 0
}
