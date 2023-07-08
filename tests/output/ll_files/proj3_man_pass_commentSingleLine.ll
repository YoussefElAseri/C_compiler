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
; // line 1
; 
; charc='\n'
%c = alloca i8
store i8 10, i8* %c
; // another line
; 
; floatf=33.1
%f = alloca float
store float 0x40408cccc0000000, float* %f
; /////// some documentation
; 
; /////////////////////////////////////
; 
; // abcdef 123 //////////
; 
; floatfinal_line=33.99895
%final_line = alloca float
store float 0x4040ffdda0000000, float* %final_line
ret i1 0
}
