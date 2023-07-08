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
; 1+1
; 0-6985
; 5*63
; 99/3622
; 3>1
; 3<1
; 8897==45647897
; +487897
; -5
; 1&&656
; 989||68779
; !65465
; 1+(3*6)/(1+3)
; 1+3+5*(62/3)
; 5*+9
; 33*-5
; ((-6))*(((5+32/(6532))))
ret i1 0
}
