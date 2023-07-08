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
; constintx=98362
%x = alloca i32
store i32 98362, i32* %x
; constint*x_ptr=&x
%x_ptr = alloca i32*
store i32* %x, i32** %x_ptr
; constint**p=&x_ptr
%p = alloca i32**
store i32** %x_ptr, i32*** %p
; constint*z=&x
%z = alloca i32*
store i32* %x, i32** %z
; constfloata=856.25668
%a = alloca float
store float 0x408ac20da0000000, float* %a
; constfloat*a_ptr=&a
%a_ptr = alloca float*
store float* %a, float** %a_ptr
ret i1 0
}
