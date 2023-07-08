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
; floatx=0.478984
%x = alloca float
store float 0x3fdea7ac80000000, float* %x
; floaty=5489451.245847
%y = alloca float
store float 0x4154f0cac0000000, float* %y
; floatf=1654.0000
%f = alloca float
store float 0x4099d80000000000, float* %f
; floatz=0000.00000
%z = alloca float
store float 0x0000000000000000, float* %z
; z=-565.21547
store float 0xc081a9b940000000, float* %z
ret i1 0
}
