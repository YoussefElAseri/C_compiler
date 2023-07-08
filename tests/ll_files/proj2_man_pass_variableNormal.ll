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
; intx=5;
%x = alloca i32
store i32 5, i32* %x
; intz=x+3;
%z = alloca i32
%1 = load i32, i32* %x
%2 = add i32 %1, 3
store i32 %2, i32* %z
; x=z*z*z*(x+x);
%3 = load i32, i32* %z
%4 = load i32, i32* %z
%5 = load i32, i32* %z
%6 = load i32, i32* %x
%7 = load i32, i32* %x
%8 = add i32 %6, %7
%9 = mul i32 %5, %8
%10 = mul i32 %4, %9
%11 = mul i32 %3, %10
store i32 %11, i32* %x
; floatf=0.986312;
%f = alloca float
store float 0x3fef8fde20000000, float* %f
; floatf2=f*33.0+2.0;
%f2 = alloca float
%12 = load float, float* %f
%13 = fmul float %12, 0x4040800000000000
%14 = fadd float %13, 0x4000000000000000
store float %14, float* %f2
; f2=f2+f;
%15 = load float, float* %f2
%16 = load float, float* %f
%17 = fadd float %15, %16
store float %17, float* %f2
; charc='a';
%c = alloca i8
store i8 97, i8* %c
; c='b';
store i8 98, i8* %c
ret i1 0
}
