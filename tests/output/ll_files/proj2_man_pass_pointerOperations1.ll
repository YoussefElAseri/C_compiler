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
; charx='a'
%x = alloca i8
store i8 97, i8* %x
; char*chr_ptr=&x
%chr_ptr = alloca i8*
store i8* %x, i8** %chr_ptr
; *chr_ptr='b'
%1 = load i8*, i8** %chr_ptr
store i8 98, i8* %1
; charanother_char=*chr_ptr
%another_char = alloca i8
%2 = load i8*, i8** %chr_ptr
%3 = load i8, i8* %2
store i8 %3, i8* %another_char
ret i1 0
}
