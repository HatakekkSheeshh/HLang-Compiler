"""
AST Generation module for CS programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.CSVisitor import CSVisitor
from build.CSParser import CSParser
from src.utils.nodes import *

class ASTGeneration(CSVisitor):
    #! program: statement* EOF;
    def visitProgram(self, ctx:CSParser.ProgramContext):
        return Program([self.visit(stmt) for stmt in ctx.statement()])

    #! type_system: INT;
    def visitType_system(self, ctx:CSParser.Type_systemContext):
        return IntType()

    #! statement: const_stmt | call_stmt;
    def visitStatement(self, ctx:CSParser.StatementContext):
        return self.visitChildren(ctx)

    #! const_stmt: CONST ID type_system? ASSIGN expression SEMICOLON;
    def visitConst_stmt(self, ctx:CSParser.Const_stmtContext):
        name = ctx.ID().getText()
        type_annotation = self.visit(ctx.type_system()) if ctx.type_system() else None
        value = self.visit(ctx.expression())
        return ConstStmt(name, type_annotation, value)

    #! call_stmt: ID LRB expression RRB SEMICOLON;
    def visitCall_stmt(self, ctx:CSParser.Call_stmtContext):
        function_name = ctx.ID().getText()
        args = self.visit(ctx.expression())
        return CallStmt(function_name, args)

    #! literal: INT_LIT;
    def visitLiteral(self, ctx:CSParser.LiteralContext):
        return IntegerLiteral(int(ctx.INT_LIT().getText()))

    #! expression:  expression PLUS expression1 | expression1;
    def visitExpression(self, ctx:CSParser.ExpressionContext):
        if ctx.getChildCount() == 3:
            left = self.visit(ctx.expression())
            operator = ctx.PLUS().getText()
            right = self.visit(ctx.expression1())
            return BinaryOp(left, operator, right)
        else:
            return self.visit(ctx.expression1())

    #! expression1: literal | ID;
    def visitExpression1(self, ctx:CSParser.Expression1Context):
        if ctx.literal():
            return self.visit(ctx.literal())
        else:
            return Identifier(ctx.ID().getText())



