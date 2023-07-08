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
; intx=4;
%x = alloca i32
store i32 4, i32* %x
; intb=9632;
%b = alloca i32
store i32 9632, i32* %b
; constint*x_ptr=&b;
%x_ptr = alloca i32*
store i32* %b, i32** %x_ptr
; *x_ptr=x;
%1 = load i32*, i32** %x_ptr
%2 = load i32, i32* %x
store i32 %2, i32* %1
ret i1 0
}
