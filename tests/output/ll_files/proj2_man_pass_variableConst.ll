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
; constintx=5
%x = alloca i32
store i32 5, i32* %x
; constfloatf=0.5487
%f = alloca float
store float 0x3fe18ef340000000, float* %f
; constinty=x*35*-5
%y = alloca i32
%1 = load i32, i32* %x
%2 = mul i32 %1, -175
store i32 %2, i32* %y
; constfloatz=f*f*f
%z = alloca float
%3 = load float, float* %f
%4 = load float, float* %f
%5 = load float, float* %f
%6 = fmul float %4, %5
%7 = fmul float %3, %6
store float %7, float* %z
ret i1 0
}
