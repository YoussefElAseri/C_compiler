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
; /*
;  * This is a comment
;  *
;  */
; /**
;  * Another Comment
;   ***** /
; 
;   /**
; 
;   *
;   *
;   **/
; intline_of_code=5
%line_of_code = alloca i32
store i32 5, i32* %line_of_code
; /* /// ** ** // // //  */
; floatf=45
%f = alloca float
store float 0x4046800000000000, float* %f
; charc='b'
%c = alloca i8
store i8 98, i8* %c
; intx=5
%x = alloca i32
store i32 5, i32* %x
ret i1 0
}
