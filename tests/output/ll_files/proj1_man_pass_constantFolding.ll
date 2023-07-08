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
; 33+69789*(69421/51213+(2231-654))
; 654*(15486-(15000+486))
; 1&&(1||0)
; 0&&(1&&1)
; 0||(0*3)
; 1&&(!(1+0))
; 12+(98721+36265/456)*(0+1687)
; 12+(98721*0+36265/456)*(0)
; (12321>(9656+3))
; (125154<(54>-65))
ret i1 0
}
