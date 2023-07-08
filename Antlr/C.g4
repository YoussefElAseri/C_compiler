grammar C;


run
    : include? (function | global_var | forward_declare | comment)* EOF;

include
    : INCLUDE STDIO;

global_var
    : instantiationExpression SEMICOLON
    | array_initialisation SEMICOLON;

function
    : function_declaration block_scope;

forward_declare
    : function_declaration SEMICOLON;

function_declaration
    : (VOID | type) IDENTIFIER LBRACKET argument_declaration? RBRACKET;

argument_declaration
    : CONST? type AMPERSAND? IDENTIFIER (COMMA argument_declaration)? ;

function_call
    : scanf
    | printf
    | IDENTIFIER LBRACKET argument? RBRACKET;

printf
    : PRINTF LBRACKET STRINGLITERAL (COMMA argument)? RBRACKET;

scanf
    : SCANF LBRACKET STRINGLITERAL (COMMA argument)? RBRACKET;

argument
    : (logicexpression | STRINGLITERAL) (COMMA argument)? ;

statement
    : comment? expression_statement SEMICOLON
    | comment? array_initialisation SEMICOLON
    | comment? jump_statement SEMICOLON
    | comment? compound_statement
    | comment? block_scope
    | comment;

array_initialisation
    : type IDENTIFIER LSQUARE INTLITERAL RSQUARE;

block_scope
    : LCURLY statement* RCURLY;

compound_statement
    : if
    | while
    | for;

expression_statement
    : assignment
    | logicexpression
    | instantiationExpression;

jump_statement
    : break
    | continue
    | return logicexpression?;

if
    : IF condition block_scope else?;

else
    : ELSE block_scope;

while
    : WHILE condition block_scope;

for
    : FOR for_condition block_scope;

break
    : BREAK;

continue
    : CONTINUE;

return
    : RETURN;

condition
    : LBRACKET logicexpression RBRACKET;

for_condition
    : LBRACKET (assignment | instantiationExpression) SEMICOLON logicexpression SEMICOLON update_expression RBRACKET;

update_expression
    : ((IDENTIFIER | pointer) EQUALS)? logicexpression;
//    | ((IDENTIFIER | pointer) EQUALS)? logicexpression COMMA update_expression;

comment
    : SINGLECOMMENT
    | MULTICOMMENT;

assignment
    : declaration EQUALS logicexpression
    | rvalue_assignment;

rvalue_assignment
    : logicexpression EQUALS logicexpression;

declaration
    : pointer
    | array
    | IDENTIFIER;

instantiationExpression
    : type not_const (COMMA not_const)*
    | CONST type const (COMMA const)*;

not_const
    : IDENTIFIER (EQUALS logicexpression)?;

const
    : IDENTIFIER EQUALS logicexpression;

type
    : (INT | CHAR | FLOAT | BOOL) STAR*;

logicexpression
    :  boolexpression (logicops (boolexpression | logicexpression))?;

boolexpression
    : term (compops (term | boolexpression))?;

term
    : factor (termops (factor | term))?;

factor
    : element (factorops (element | factor))?;

element
    : IDENTIFIER | array | LBRACKET logicexpression RBRACKET
    | (IDENTIFIER | array| LBRACKET pointer RBRACKET) SPECIALUNARY
    | SPECIALUNARY (IDENTIFIER | array | LBRACKET pointer RBRACKET)
    | pointer
    | literal
    | function_call
    | (typecast | unaryops) element;

array
    : IDENTIFIER LSQUARE logicexpression RSQUARE;

logicops
    : LOGICOPS;

compops
    : COMPOPS;

termops
    : MINUS
    | PLUS;

factorops
    : STAR
    | DIVIDE
    | PROCENT;

unaryops
    : MINUS | PLUS | EXCLAMAION | AMPERSAND;

typecast
    : LBRACKET (INT | CHAR | FLOAT | BOOL) RBRACKET;

pointer
    : STAR IDENTIFIER
    | STAR pointer;

literal
    : BOOLLITERAL
    | INTLITERAL
    | FLOATLITERAL
    | CHARLITERAL;

VOID: 'void';

IF: 'if';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';

PRINTF: 'printf';
SCANF: 'scanf';

COMPOPS
    : '<' | '>' | '<=' | '>=' | '==' | '!=';

LOGICOPS
    : '&&' | '||';

EQUALS : '=';
SEMICOLON: ';';
LBRACKET: '(';
RBRACKET: ')';
LCURLY: '{';
RCURLY: '}';
LSQUARE: '[';
RSQUARE: ']';
COMMA: ',';
DOT: '.';

PLUS : '+';
MINUS : '-';
STAR : '*';
DIVIDE : '/';
EXCLAMAION : '!';
AMPERSAND : '&';
PROCENT : '%';
HASH: '#';

SPECIALUNARY
    : '++' | '--';

INT : 'int';
CHAR : 'char';
BOOL : 'bool';
FLOAT : 'float';
CONST : 'const';

INCLUDE : '#include';
STDIO : '<stdio.h>';

IDENTIFIER
    : ('_' | [a-zA-Z]) ('_' | [0-9] | [a-zA-Z])*;

INTLITERAL
    : DIGIT+;

FLOATLITERAL
    : DIGIT+ (COMMA | DOT) DIGIT+;

CHARLITERAL
    : '\'' '\\'? . '\'';

STRINGLITERAL
    : '"' .*? '"';

BOOLLITERAL
    : 'true' | 'false';

SINGLECOMMENT
    : '//' ~[\r\n]* ('\r' | '\n')?;

MULTICOMMENT
    : '/*' .*? '*/';

fragment DIGIT: [0-9];

WS: [ \t\r\n]+ -> skip;

ANY : .;