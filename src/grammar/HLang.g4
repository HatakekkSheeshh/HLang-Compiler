grammar HLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// =============================================================== Lexer =============================================================== //
// Keyword
BOOL: 'bool';
BREAK: 'break';
CONST: 'const';
CONT: 'continue';
ELSE: 'else';
FALSE: 'false';
FLOAT: 'float';
FOR: 'for';
FUNC: 'func';
IF: 'if';
IN: 'in';
INT: 'int';
LET: 'let';
RETURN: 'return';
STR: 'string';
TRUE: 'true';
VOID: 'void';
WHILE: 'while';


// Operators
// Arithmetic
ADD: '+' ;
SUB: '-' ;
MUL: '*' ;
DIV: '/' ;
MOD: '%';

// Comparision
EQ_EQ: '==' ;
NOT_EQ: '!=' ;
LESS_EQUAL: '<=' ;
LESS_THAN: '<' ;
GREATER_THAN: '>' ;
GREATER_EQUAL: '>=' ;

// Logical
AND: '&&' ;
OR: '||' ;
NOT: '!' ;

// Assignment
ASSIGN: '=' ;

// Type annotation
TYPE_ANNOT: ':';

// Function return type
FUNC_TYPE: '->';

// PIPELINE
PLINE: '>>' ; 

// Separators
LP: '(' ;
RP: ')' ;

LSB: '[' ;
RSB: ']' ;

LB: '{' ;
RB: '}' ;

CM: ',' ;
SC: ';' ;
DOT: '.' ;

// Literals
fragment DIGIT: [0-9] ;

// Integer literals
fragment VALID_INT:  DIGIT+ ;
INT_LIT: VALID_INT ;

// Float literals
fragment EXP: [eE] [+-]? VALID_INT;
fragment DEC: '.' VALID_INT? ;
FLOAT_LIT: VALID_INT DEC EXP? ;
    
// String literals:
fragment VALID_CHAR: ~["\r\n\\] | ESC_SEQ ; 
ESC_SEQ: '\\' [tnr\\"] ;
STR_LIT: '"' VALID_CHAR* '"' { self.text = self.text[1:-1]; };

// Identifier
ID: [a-zA-Z_][a-zA-Z0-9_]*;

// =============================================================== Parser =============================================================== //
program  : constdeclList funcdeclList EOF ;
constdeclList: constdecl constdeclList | ;
funcdeclList: funcdecl funcdeclList | ;

// ================================ TYPE ================================   //
type: INT | FLOAT | BOOL | STR ;                                            //
// Annot type                                                               //
// declaration for var                                                      //
typeDecl: TYPE_ANNOT type ;                                                 //
// declaration for array: : let empty: [int; 0] = [];                       //
arrtypeDecl: TYPE_ANNOT arrtypeList ;                                       //
array_type: (type | arrtypeList) SC INT_LIT ;                               //
arrtypeList: LSB array_type RSB ;                                           //
// ================================ TYPE ================================   //           

// ================================ Declared in Program ================================    //
// const declaration                                                                        //
// const <identifier> [: <type>] = <expression>;                                            //
constdecl: CONST ID (typeDecl | arrtypeDecl)? ASSIGN expr SC ;                              //
                                                                                            //
// function declaration                                                                     //
// (param_types...) -> return_type                                                          //
funcdecl: FUNC ID LP paramList? RP return_type body ;                                       //                                                                   
paramdecl: ID (typeDecl | arrtypeDecl) ;                                                    //
paramList: paramdecl CM paramList | paramdecl;                                              //
return_type: FUNC_TYPE (type | VOID | arrtypeList) ;                                        //
// Body of function                                                                         //
body: LB mList RB ;                                                                         //
mList: (stmt | expr SC) mList | ;                                                           //
// ================================ Declared in Program ================================    //

// ================================ Statements in function =================================    //
// ASSIGNMENT                                                                                   //
assignment: lvalue ASSIGN expr SC ;                                                             //
lvalue: ID | ID LSB expr RSB | lvalue LSB expr RSB ;                                            //
                                                                                                //
// RETURN                                                                                       //
return: (RETURN expr | RETURN) SC ;                                                             //
                                                                                                //
// VARIABLE DECLARATION: let <identifier> [: <type>] = <expression>                             //
vardecl: LET ID (typeDecl | arrtypeDecl)? ASSIGN expr SC ;                                      //
                                                                                                //
// Conditional Statements                                                                       //
/*                                                                                              //
    if (condition_expression) { statements }                                                    //
    [else if (condition_expression) { statements }]*                                            //
    [else { statements }]?                                                                      //
*/                                                                                              //
cond_stmt: if_stmt elif_stmt? else_stmt? ;                                                      //
if_stmt: IF LP expr RP block_stmt ;                                                             //
elif_decl: ELSE IF LP expr RP block_stmt ;                                                      //
elif_stmt: elif_decl elif_stmt | elif_decl ;                                                    //                                   
else_stmt: ELSE block_stmt ;                                                                    //
                                                                                                //
// LOOP STATEMENTS                                                                              //
// while                                                                                        //
while: WHILE LP expr RP block_stmt ;                                                            //
// for                                                                                          //
for: FOR LP ID IN expr RP block_stmt ;                                                          //
// Break, Continue stmt                                                                         //
break_stmt: BREAK SC ;                                                                          //
cont_stmt: CONT SC ;                                                                            //
// BLock stmt                                                                                   //
block_member: (stmt | expr SC) block_member | ;                                                 //
block_stmt: LB block_member RB ;                                                                //
                                                                                                //
// STATMENTS                                                                                    //
stmt: vardecl                                                                                   //
    | assignment                                                                                //
    | cond_stmt                                                                                 //
    | while                                                                                     //
    | for                                                                                       // 
    | return                                                                                    //
    | break_stmt                                                                                //
    | cont_stmt                                                                                 //
    | block_stmt                                                                                //
    ;
// ================================ Statements in function =================================    //

// ==================================== Expression ==================================== // 
// CALL                                                                                         
// len(), str(), int(), float(), input(), print()...                                            
callList: expr CM callList | expr;                                                                                                                                            
call: (ID | INT | FLOAT) LP (callList | ) RP  ;                                                 

arr_elements: expr CM arr_elements | expr ; // (expr | ) | e , es

// EXPR stmt
expr: expr PLINE expr1 | expr1 ;
expr1: expr1 OR expr2 | expr2 ;
expr2: expr2 AND expr3 | expr3 ;
expr3: expr3 EQ_EQ expr4 | expr3 NOT_EQ expr4 | expr4 ;
expr4: expr4 LESS_THAN expr5 
    | expr4 LESS_EQUAL expr5
    | expr4 GREATER_THAN expr5
    | expr4 GREATER_EQUAL expr5
    | expr5
    ;
expr5: expr5 ADD expr6 | expr5 SUB expr6 | expr6 ;
expr6: expr6 MUL expr7 | expr6 DIV expr7 | expr6 MOD expr7 | expr7 ;
expr7: SUB expr7 | NOT expr7 | ADD expr7 | expr8 ;
expr8: expr8 LSB expr RSB | expr9 ;
expr9:  
    LP expr RP 
    | literals 
    | ID 
    | call 
    | LSB (arr_elements | ) RSB
    ; 

// literals
literals: INT_LIT | FLOAT_LIT | STR_LIT | TRUE | FALSE ;


// Skip
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs 
fragment LINE_CMT: '//' ~[\r\n]*;
fragment BLOCK_CMT: '/*' (BLOCK_CMT | .)*? '*/';
CMT: (LINE_CMT | BLOCK_CMT)  -> skip ;

// Throw error
ERROR_CHAR: .;
fragment ESC_ILLEGAL: '\\' ~[ntr"\\];
ILLEGAL_ESCAPE: '"' VALID_CHAR* ESC_ILLEGAL  { self.text = self.text[1:] ; } ;
UNCLOSE_STRING: '"' VALID_CHAR* ('\r\n' | '\n' | EOF) { self.text = self.text[1:] ; } ;
