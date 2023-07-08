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
; floatf=33989.586265;
%f = alloca float
store float 0x40e098b2c0000000, float* %f
; intz=(int)f;
%z = alloca i32
%1 = load float, float* %f
%2 = fptosi float %1 to i32
store i32 %2, i32* %z
; floatz2=(float)x;
%z2 = alloca float
%3 = load i32, i32* %x
%4 = sitofp i32 %3 to float
store float %4, float* %z2
; inta=(int)(f+z2*2);
%a = alloca i32
%5 = load float, float* %f
%6 = load float, float* %z2
%7 = sitofp i32 2 to float
%8 = fmul float %6, %7
%9 = fadd float %5, %8
%10 = fptosi float %9 to i32
store i32 %10, i32* %a
; floatf2=(float)f;
%f2 = alloca float
%11 = load float, float* %f
store float %11, float* %f2
; f2=(float)(a+z2/(3*65232));
%12 = load i32, i32* %a
%13 = load float, float* %z2
%14 = sitofp i32 195696 to float
%15 = fdiv float %13, %14
%16 = sitofp i32 %12 to float
%17 = fadd float %16, %15
store float %17, float* %f2
ret i1 0
}
