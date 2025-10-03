"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *

class ASTGeneration(HLangVisitor):
    # =============================================================== Parser =============================================================== #
    # Visit a parse tree produced by HLangParser#program.
    # ================================ TYPE ================================   #
    def visitProgram(self, ctx:HLangParser.ProgramContext):
        const_decls = self.visit(ctx.constdeclList())
        func_decls = self.visit(ctx.funcdeclList())
        return Program(const_decls, func_decls)


    # Visit a parse tree produced by HLangParser#constdeclList.
    def visitConstdeclList(self, ctx:HLangParser.ConstdeclListContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.constdecl())] + self.visit(ctx.constdeclList())


    # Visit a parse tree produced by HLangParser#funcdeclList.
    def visitFuncdeclList(self, ctx:HLangParser.FuncdeclListContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.funcdecl())] + self.visit(ctx.funcdeclList())


    # Visit a parse tree produced by HLangParser#type.
    def visitType(self, ctx:HLangParser.TypeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOL():
            return BoolType()
        elif ctx.STR():
            return StringType()
        return None


    # Visit a parse tree produced by HLangParser#typeDecl.
    def visitTypeDecl(self, ctx:HLangParser.TypeDeclContext):
        return self.visit(ctx.type_())

    # Visit a parse tree produced by HLangParser#arrtypeDecl.
    def visitArrtypeDecl(self, ctx:HLangParser.ArrtypeDeclContext):
        return self.visit(ctx.arrtypeList())


    # Visit a parse tree produced by HLangParser#array_type.
    def visitArray_type(self, ctx:HLangParser.Array_typeContext):
        if ctx.type_():
            return self.visit(ctx.type_()), ctx.INT_LIT()
        elif ctx.arrtypeList():
            return self.visit(ctx.arrtypeList()), ctx.INT_LIT()
        return None

    # Visit a parse tree produced by HLangParser#arrtypeList.
    def visitArrtypeList(self, ctx:HLangParser.ArrtypeListContext):
        if ctx.array_type():
            return ArrayType(*self.visit(ctx.array_type()))
        return None

    # ================================== Const ================================== #
    # Visit a parse tree produced by HLangParser#constdecl.
    def visitConstdecl(self, ctx:HLangParser.ConstdeclContext):
        # constdecl: CONST ID typeDecl ASSIGN expr SC 
        name = ctx.ID().getText()
        type_ = None 
        if ctx.typeDecl():
            type_ = self.visit(ctx.typeDecl())
        elif ctx.arrtypeDecl():
            type_ = self.visit(ctx.arrtypeDecl())
        value = self.visit(ctx.expr())

        return ConstDecl(name, type_, value)


    # ================================== funcdecl: FUNC id_func return_type body SC; ================================== #
    # Visit a parse tree produced by HLangParser#funcdecl.
    def visitFuncdecl(self, ctx:HLangParser.FuncdeclContext):
        # funcdecl: FUNC ID LP paramList? RP return_type body ;  
        name = ctx.ID().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        return_type = self.visit(ctx.return_type())
        body = self.visit(ctx.body())
        return FuncDecl(name, params, return_type, body)

    # Visit a parse tree produced by HLangParser#paramdecl.
    def visitParamdecl(self, ctx:HLangParser.ParamdeclContext):
        name = ctx.ID().getText()
        if ctx.typeDecl():
            type_ = self.visit(ctx.typeDecl())
        elif ctx.arrtypeDecl():
            type_ = self.visit(ctx.arrtypeDecl())

        return Param(name, type_)

    # Visit a parse tree produced by HLangParser#paramList.
    def visitParamList(self, ctx:HLangParser.ParamListContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.paramdecl())] 
        return [self.visit(ctx.paramdecl())] + self.visit(ctx.paramList())
    
    # Visit a parse tree produced by HLangParser#return_type.
    def visitReturn_type(self, ctx:HLangParser.Return_typeContext):
        if ctx.VOID():
            return VoidType()
        return_type = [ctx.type_, ctx.arrtypeList]
        return next(self.visit(rety()) for rety in return_type if rety())
    # ====================== BODY ====================== #
    # Visit a parse tree produced by HLangParser#body.
    def visitBody(self, ctx:HLangParser.BodyContext):
        return self.visit(ctx.mList())

    # Visit a parse tree produced by HLangParser#mList.
    def visitMList(self, ctx:HLangParser.MListContext):
        if ctx.getChildCount() == 0:
            return []
        if ctx.stmt():
            return [self.visit(ctx.stmt())] + self.visit(ctx.mList())
        elif ctx.expr():
            return [ExprStmt(self.visit(ctx.expr()))] + self.visit(ctx.mList())
        return None
    
    # ================================ Statements in function =================================    #
    # ====================== Statement ====================== #
    # Visit a parse tree produced by HLangParser#assignment.
    # ASSIGNMENT    
    def visitAssignment(self, ctx:HLangParser.AssignmentContext):
        return Assignment(self.visit(ctx.lvalue()), self.visit(ctx.expr()))

    # Visit a parse tree produced by HLangParser#lvalue.
    def visitLvalue(self, ctx:HLangParser.LvalueContext):
        # ID | ID LSB expr RSB
        if ctx.ID():
            if ctx.LSB():
                return ArrayAccessLValue(Identifier(ctx.ID().getText()), self.visit(ctx.expr()))
            else:
                return IdLValue(ctx.ID().getText())
        
        """
        - Instruction: [lvalue LSB expr RSB]
        - Recursive: lvalue[expr]
        """
        inner_ctx = ctx.lvalue()
        # Base case
        if inner_ctx.ID():
            if inner_ctx.LSB():
                inner_ast = ArrayAccess(Identifier(inner_ctx.ID().getText()), self.visit(inner_ctx.expr()))
            else:
                inner_ast = Identifier(inner_ctx.ID().getText())
        else:
            inner_lvalue = self.visit(inner_ctx)
            if isinstance(inner_lvalue, ArrayAccessLValue):
                inner_ast = ArrayAccess(inner_lvalue.array, inner_lvalue.index)
            elif isinstance(inner_lvalue, IdLValue):
                inner_ast = Identifier(inner_lvalue.name)
            else: inner_ast = inner_lvalue
        return ArrayAccessLValue(inner_ast, self.visit(ctx.expr()))        


    # CALL  
    # Visit a parse tree produced by HLangParser#callList.
    def visitCallList(self, ctx:HLangParser.CallListContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.expr())]
        return [self.visit(ctx.expr())] + self.visit(ctx.callList())

    # Visit a parse tree produced by HLangParser#call.
    def visitCall(self, ctx:HLangParser.CallContext):
        if ctx.ID():
            id = ctx.ID().getText()
        elif ctx.INT():
            id = ctx.INT().getText()
        elif ctx.FLOAT():
            id = ctx.FLOAT().getText()
        return FunctionCall(Identifier(id), self.visit(ctx.callList()) if ctx.callList() else [])


    # RETURN
    # Visit a parse tree produced by HLangParser#return.
    def visitReturn(self, ctx:HLangParser.ReturnContext):
        if not ctx.expr():
            return ReturnStmt()
    
        return ReturnStmt(self.visit(ctx.expr()))


    # Visit a parse tree produced by HLangParser#vardecl.
    def visitVardecl(self, ctx:HLangParser.VardeclContext):
        name = ctx.ID().getText()

        # Inference type
        if ctx.typeDecl():
            type_ = self.visit(ctx.typeDecl())
        elif ctx.arrtypeDecl():
            type_ = self.visit(ctx.arrtypeDecl())
        else:
            type_ = None 
        
        value = self.visit(ctx.expr())

        return VarDecl(name, type_, value) 


    # IF ELSE 
    # Visit a parse tree produced by HLangParser#cond_stmt.
    def visitCond_stmt(self, ctx:HLangParser.Cond_stmtContext):
        if_st, then_stmt = self.visit(ctx.if_stmt())
        elif_st = self.visit(ctx.elif_stmt()) if ctx.elif_stmt() else []
        else_st = self.visit(ctx.else_stmt()) if ctx.else_stmt() else None
        return IfStmt(if_st, then_stmt, elif_st, else_st)


    # Visit a parse tree produced by HLangParser#if_stmt.
    def visitIf_stmt(self, ctx:HLangParser.If_stmtContext):
        return self.visit(ctx.expr()), self.visit(ctx.block_stmt())


    # Visit a parse tree produced by HLangParser#elif_decl.
    def visitElif_decl(self, ctx:HLangParser.Elif_declContext):
        return self.visit(ctx.expr()), self.visit(ctx.block_stmt())


    # Visit a parse tree produced by HLangParser#elif_stmt.
    def visitElif_stmt(self, ctx:HLangParser.Elif_stmtContext):
        if ctx.getChildCount() == 1: 
            return [self.visit(ctx.elif_decl())]
        return [self.visit(ctx.elif_decl())] + self.visit(ctx.elif_stmt())


    # Visit a parse tree produced by HLangParser#else_stmt.
    def visitElse_stmt(self, ctx:HLangParser.Else_stmtContext):
        return self.visit(ctx.block_stmt())

    # WHILE
    # Visit a parse tree produced by HLangParser#while.
    def visitWhile(self, ctx:HLangParser.WhileContext):
        return WhileStmt(self.visit(ctx.expr()), self.visit(ctx.block_stmt()))

    # FOR
    # Visit a parse tree produced by HLangParser#for.
    def visitFor(self, ctx:HLangParser.ForContext):
        return ForStmt(ctx.ID().getText(), self.visit(ctx.expr()), self.visit(ctx.block_stmt()))

    # BREAK
    # Visit a parse tree produced by HLangParser#break_stmt.
    def visitBreak_stmt(self, ctx:HLangParser.Break_stmtContext):
        return BreakStmt()

    # CONTINUE
    # Visit a parse tree produced by HLangParser#cont_stmt.
    def visitCont_stmt(self, ctx:HLangParser.Cont_stmtContext):
        return ContinueStmt()

    # BLOCK
    # Visit a parse tree produced by HLangParser#block_member.
    def visitBlock_member(self, ctx:HLangParser.Block_memberContext):
        if ctx.getChildCount() == 0:
            return []
        if ctx.stmt():
            return [self.visit(ctx.stmt())] + self.visit(ctx.block_member()) 
        elif ctx.expr():
            return [ExprStmt(self.visit(ctx.expr()))] + self.visit(ctx.block_member())
        return []
        

    # Visit a parse tree produced by HLangParser#block_stmt.
    def visitBlock_stmt(self, ctx:HLangParser.Block_stmtContext):
        return BlockStmt(self.visit(ctx.block_member()))


    # Visit a parse tree produced by HLangParser#stmt.
    def visitStmt(self, ctx:HLangParser.StmtContext):
        stmt_getters = [
            ctx.vardecl,
            ctx.assignment,
            ctx.cond_stmt,
            ctx.while_,
            ctx.for_,
            ctx.return_,
            ctx.break_stmt,
            ctx.cont_stmt,
            ctx.block_stmt,
        ]
    
        return next(
            (self.visit(getter()) for getter in stmt_getters if getter()),
            None
        )

    # ======================================== Array ======================================== #
    # Visit a parse tree produced by HLangParser#arr_elements.
    def visitArr_elements(self, ctx:HLangParser.Arr_elementsContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.expr())]
        return [self.visit(ctx.expr())] + self.visit(ctx.arr_elements())


    # ======================================== Expression ======================================== #
    # Visit a parse tree produced by HLangParser#expr.
    # expr: expr PLINE expr1 | expr1 ;
    def visitExpr(self, ctx:HLangParser.ExprContext):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        return BinaryOp(self.visit(ctx.expr()), ctx.PLINE().getText() , self.visit(ctx.expr1()))


    # Visit a parse tree produced by HLangParser#expr1.
    def visitExpr1(self, ctx:HLangParser.Expr1Context):
        # expr1: expr1 OR expr2 | expr2 ;
        if ctx.getChildCount() == 1: 
            return self.visitChildren(ctx)

        return BinaryOp(self.visit(ctx.expr1()), ctx.OR().getText(), self.visit(ctx.expr2()))


    # Visit a parse tree produced by HLangParser#expr2.
    def visitExpr2(self, ctx:HLangParser.Expr2Context):
        # expr2: expr2 AND expr3 | expr3 ;
        if ctx.getChildCount() == 1: 
            return self.visitChildren(ctx)

        return BinaryOp(self.visit(ctx.expr2()), ctx.AND().getText(), self.visit(ctx.expr3()))


    # Visit a parse tree produced by HLangParser#expr3.
    def visitExpr3(self, ctx:HLangParser.Expr3Context):
        # expr3: expr3 EQ_EQ expr4 | expr3 NOT_EQ expr4 | expr4 ;
        if ctx.getChildCount() == 1: 
            return self.visitChildren(ctx)
        if ctx.EQ_EQ():
            op = ctx.EQ_EQ().getText()
        elif ctx.NOT_EQ():
            op = ctx.NOT_EQ().getText()

        return BinaryOp(self.visit(ctx.expr3()), op, self.visit(ctx.expr4()))


    # Visit a parse tree produced by HLangParser#expr4.
    def visitExpr4(self, ctx:HLangParser.Expr4Context):
        """
        expr4: expr4 LESS_THAN expr5 
            | expr4 LESS_EQUAL expr5
            | expr4 GREATER_THAN expr5
            | expr4 GREATER_EQUAL expr5
            | expr5
            ; 
        """
        if ctx.getChildCount() == 1: 
            return self.visitChildren(ctx)
        if ctx.LESS_THAN():
            op = ctx.LESS_THAN().getText()
        elif ctx.LESS_EQUAL():
            op = ctx.LESS_EQUAL().getText()
        elif ctx.GREATER_THAN():
            op = ctx.GREATER_THAN().getText()
        elif ctx.GREATER_EQUAL():
            op = ctx.GREATER_EQUAL().getText()

        return BinaryOp(self.visit(ctx.expr4()), op, self.visit(ctx.expr5()))


    # Visit a parse tree produced by HLangParser#expr5.
    def visitExpr5(self, ctx:HLangParser.Expr5Context):
        # expr5 ADD expr6 | expr5 SUB expr6 | expr6 ;
        if ctx.ADD():
            op = ctx.ADD().getText()
        elif ctx.SUB():
            op = ctx.SUB().getText()
    
        if ctx.getChildCount() == 1: 
            return self.visitChildren(ctx)
        return BinaryOp(self.visit(ctx.expr5()), op, self.visit(ctx.expr6()))


    # Visit a parse tree produced by HLangParser#expr6.
    def visitExpr6(self, ctx:HLangParser.Expr6Context):
        # expr6 MUL expr7 | expr6 DIV expr7 | expr6 MOD expr7 | expr7 ;
        if ctx.getChildCount() == 1: 
            return self.visitChildren(ctx)
        if ctx.MUL():
            op = ctx.MUL().getText()
        elif ctx.DIV():
            op = ctx.DIV().getText()
        elif ctx.MOD():
            op = ctx.MOD().getText()

        return BinaryOp(self.visit(ctx.expr6()), op, self.visit(ctx.expr7()))


    # Visit a parse tree produced by HLangParser#expr7.
    def visitExpr7(self, ctx:HLangParser.Expr7Context):
        # SUB expr7 | NOT expr7 | ADD expr7 | expr8 ;
        if ctx.getChildCount() == 1: 
            return self.visitChildren(ctx)
        if ctx.SUB():
            op = ctx.SUB().getText()
        elif ctx.NOT():
            op = ctx.NOT().getText()
        elif ctx.ADD():
            op = ctx.ADD().getText()
        
        return UnaryOp(op, self.visit(ctx.expr7()))


    # Visit a parse tree produced by HLangParser#expr8.
    def visitExpr8(self, ctx:HLangParser.Expr8Context):
        # expr8: expr8 LSB expr RSB | expr9 ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr9())

        return ArrayAccess(self.visit(ctx.expr8()), self.visit(ctx.expr()))
    
    # Visit a parse tree produced by HLangParser#expr9.
    def visitExpr9(self, ctx:HLangParser.Expr9Context):
        # expr9: LP expr RP | literals | ID | call | array | input | arr_name ; 
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.literals():
            return self.visit(ctx.literals())
        elif ctx.call():
            return self.visit(ctx.call())
        elif ctx.LSB() and ctx.RSB():
            if ctx.arr_elements():
                return ArrayLiteral(self.visit(ctx.arr_elements()))
            else:
                return ArrayLiteral([])
        elif ctx.LP() and ctx.RP():
            return self.visit(ctx.expr())

    # ====================== Literals ====================== #
    # Visit a parse tree produced by HLangParser#literals.
    def visitLiterals(self, ctx:HLangParser.LiteralsContext):
        if ctx.INT_LIT():
            return IntegerLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STR_LIT():
            return StringLiteral(str(ctx.STR_LIT().getText()))
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
