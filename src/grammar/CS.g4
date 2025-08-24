grammar CS;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.ERROR_CHAR:
        result = super().emit()
        raise ErrorToken(result.text)
    else:
        return super().emit()
}

options{
	language=Python3;
}


//--------------------------------LEXER------------------------------//
// KEYWORDS
CONST: 'const';
INT: 'int';

// OPERATORS
PLUS: '+';
ASSIGN: '=';

// SEPARATOR
LRB: '(';
RRB: ')';
SEMICOLON: ';';

//IDENTIFIERS
ID: [a-zA-Z_][a-zA-Z0-9_]*;

// LITERAL
INT_LIT: [0-9]+;

// COMMENT, WHITE SPACE
SINGLE_COMMENT: '//' ~[\r\n]* -> skip;
WS: [ \t\r\n]+ -> skip;

// ERROR
ERROR_CHAR: .;
//--------------------------------LEXER------------------------------//

// declared 
program: statement* EOF;

// Type
type_system: INT;

// Statement
statement: const_stmt | call_stmt;

const_stmt: CONST ID type_system? ASSIGN expression SEMICOLON;
call_stmt: ID LRB expression RRB SEMICOLON;

// Expressions 
literal: INT_LIT;

expression:  expression PLUS expression1 | expression1;
expression1: literal | ID;

