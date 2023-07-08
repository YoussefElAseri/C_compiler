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
; intinteger=5;
%integer = alloca i32
store i32 5, i32* %integer
; int*int_ptr=&integer;
%int_ptr = alloca i32*
store i32* %integer, i32** %int_ptr
; int**ptr_ptr=&int_ptr;
%ptr_ptr = alloca i32**
store i32** %int_ptr, i32*** %ptr_ptr
; int**another_pointer=ptr_ptr;
%another_pointer = alloca i32**
%1 = load i32**, i32*** %ptr_ptr
store i32** %1, i32*** %another_pointer
; intz=integer+5;
%z = alloca i32
%2 = load i32, i32* %integer
%3 = add i32 %2, 5
store i32 %3, i32* %z
; int_ptr=&z;
store i32* %z, i32** %int_ptr
; int*pointer=&z;
%pointer = alloca i32*
store i32* %z, i32** %pointer
; intx=*pointer;
%x = alloca i32
%4 = load i32*, i32** %pointer
%5 = load i32, i32* %4
store i32 %5, i32* %x
; int**x_ptr=&int_ptr;
%x_ptr = alloca i32**
store i32** %int_ptr, i32*** %x_ptr
ret i1 0
}
