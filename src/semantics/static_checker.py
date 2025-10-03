"""
Static Semantic Checker for CS Programming Language
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)
  
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker

class FunctionType(Type):
    """
    Function type node, example:
        (IntType, FloatType) -> BoolType
    Thuộc tính:
        param_types : List[Type]    - list of paramters' type
        return_type : Type          - return type
        forward_declaration: Bool   - forward declaration flag
    """
    def __init__(self, param_types: List[Type], return_type: Type, forward_declaration: bool = False):
        super().__init__()
        self.param_types = param_types
        self.return_type = return_type
        self.forward_declaration = forward_declaration

    def accept(self, visitor):
        pass

    def __str__(self):
        params_str = ', '.join(str(t) for t in self.param_types) if self.param_types else ""
        params_part = f"({params_str})" if params_str else "()"
        return f"FunctionType{params_part} -> {self.return_type}"
    
class Symbol:
    """
    Represents a named entity in the program with associated type information.
    Typically used for variables, constants, and function declarations.
    """
    def __init__(self, name: str, typ: 'Type', isConst: bool = False):
        """
        :param name: The identifier's name (e.g., variable or function name).
        :param typ: The type associated with the symbol (e.g., IntType, BoolType).
        """
        self.name = name  # The symbol's name
        self.typ = typ    # The type information (from AST type system)
        self.isConst = isConst
    """
    let x: int;
    print(Symbol(x, int)) -> Symbol(name=x,type=int)
    """
    def __str__(self):
        return f"Symbol(name={self.name}, type={self.typ})"
    
    @staticmethod
    def str(params: List[List['Symbol']]) -> str:
        """
        Convert a list of symbol lists (e.g., representing parameters in nested scopes)
        into a readable string representation.
            :param params: A 2D list of Symbol objects.
            :return: A formatted string.
        params = [[scope_1], [scope_2],...]
        print(Symbol.str(params))
        """
        return "[" + ", ".join(
            "[" + ", ".join(str(sym) for sym in scope) + "]"
            for scope in params
        ) + "]"
    
class StaticChecker(ASTVisitor):
    """
    Redeclared - Variables, constants, functions, or parameters declared multiple times in the same scope
    Undeclared - Use of identifiers or functions that have not been declared
    MustInLoop - Break/continue statements outside of loop contexts
    NoEntryPoint - Missing or invalid main function
    """
    def __init__(self):
        self.number_loop = 0
        self.current_function = None
        self.in_expr_stmt = False
        self.isFor = False

    def lookup(self, name: str, lst: List, func):
        """
        Find and return the first element in the list for which the given function
        returns a value equal to `name`.
        Args:
            name (str): The value to match.
            lst (List): A list of elements to search.
            func (Callable): A function that extracts a comparable value from each element.
        Returns:
            Any: The first element `x` in `lst` such that `func(x) == name`, or `None` if not found.
        """
        for x in lst:
            if name == func(x):
                return x
        return None

    def type_compatible(self, expected_type: Type, actual_type: Optional[Type]) -> bool:
        """
        Args:
            expected_type: The declared/expected type
            actual_type: The inferred type from expression    
        """
        if actual_type is None:
            return False
            
        if type(expected_type) == type(actual_type):
            if isinstance(expected_type, ArrayType) and isinstance(actual_type, ArrayType):
                return (self.type_compatible(expected_type.element_type, actual_type.element_type) 
                       and int(str(expected_type.size)) == int(str(actual_type.size)))
            return True
        return False
 
    def visit(self, node: 'ASTNode', param):
        return node.accept(self, param)

    def check_program(self, node: 'ASTNode'):
        self.visit(node, [])


    def visit_program(self, node: 'Program', param):
        global_env = [
                Symbol("print", FunctionType([StringType()], VoidType())),
                Symbol("input", FunctionType([], StringType())),
                Symbol("int2str", FunctionType([IntType()], StringType())),
                Symbol("float2str", FunctionType([FloatType()], StringType())),
                Symbol("bool2str", FunctionType([BoolType()], StringType())),
                Symbol("str2int", FunctionType([StringType()], IntType())),
                Symbol("str2float", FunctionType([StringType()], FloatType())),
                Symbol("len", FunctionType([ArrayType(IntType(), -1)], IntType())),
            ]

        
        global_env = reduce(
            lambda acc, ele: [([self.visit(ele, acc)] + acc[0])] + acc[1:], 
            node.const_decls, 
            [global_env]
        )[0] 

        for func in node.func_decls:
            forward_declare = True 
            symbol = self.lookup(func.name, global_env, lambda x: x.name)
            if symbol:
                forward_declare = False
            func_signature = Symbol(
                name = func.name,
                typ = FunctionType(
                    list(map(lambda x: x.param_type, func.params)),
                    func.return_type,
                    forward_declare
                )
            )
            global_env = [func_signature] + global_env

        # NoEntryPoint
        if not any((func.name == "main" and not func.params and isinstance(func.return_type, VoidType)) for func in node.func_decls):
            raise NoEntryPoint()

        # const_decls, func_decls in nodes of Program 
        reduce(
            lambda acc, ele: [([self.visit(ele, acc)] + acc[0])] + acc[1:], 
            node.func_decls, 
            [global_env]
        ) 


    def visit_const_decl(self, node: 'ConstDecl', param: List[List['Symbol']]) -> Symbol:
        symbol = self.lookup(node.name, param[0], lambda x: x.name)
        if symbol:
            is_function = isinstance(symbol.typ, FunctionType)
            if is_function:
                if not symbol.typ.forward_declaration:
                    raise Redeclared('Constant', node.name)
            else:
                raise Redeclared('Constant', node.name)

        type_ = self.visit(node.value, param)
        if node.type_annotation:                
            if type_:
                if not self.type_compatible(node.type_annotation, type_):
                    raise TypeMismatchInStatement(node)
            else:
                if isinstance(node.type_annotation, ArrayType):
                    if not int(str(node.type_annotation.size)) == 0:
                        raise TypeMismatchInStatement(node)

            type_ = node.type_annotation

        if not type_:
            raise TypeCannotBeInferred(node)

        return Symbol(node.name, type_, True)


    def visit_func_decl(self, node: 'FuncDecl', param: List[List['Symbol']]):
        """
        func_decl:
        def __init__(self, name: str, params: List['Param'], return_type: 'Type', body: List['Stmt']):
            super().__init__()
            self.name = name
            self.params = params
            self.return_type = return_type
            self.body = body
        """
        # Redeclared with other function name or Built-in function
        symbol = self.lookup(node.name, param[0], lambda x: x.name)

        if symbol:
            is_function = isinstance(symbol.typ, FunctionType)
            if is_function:
                if not symbol.typ.forward_declaration:
                    raise Redeclared('Function', node.name)
            else:
                raise Redeclared('Function', node.name)
        """
        new scope ([[]]) + global scope (param)
        """
        self.current_function = node
        # Add parameters to current scope and check Redeclared
        params = reduce(lambda acc, ele: [self.visit(ele, acc)] + acc, node.params, [])
        # Check body
        reduce(
            lambda acc, ele: [([result] + acc[0]) if isinstance(result := self.visit(ele, acc), Symbol) else acc[0]] + acc[1:], 
            node.body, 
            [params] + param
        )
        return Symbol(node.name, FunctionType(list(map(lambda param: param.param_type, node.params)), node.return_type))


    def visit_param(self, node: 'Param', param: List['Symbol']) -> Symbol:
        symbol = self.lookup(node.name, param, lambda x: x.name)
        if symbol:
            raise Redeclared('Parameter', node.name)
        return Symbol(node.name, node.param_type, True)


    # Statements
    def visit_var_decl(self, node: 'VarDecl', param: List[List['Symbol']]) -> Symbol:
        # Checking Redeclared
        symbol = self.lookup(node.name, param[0], lambda x: x.name)
        if symbol:
            raise Redeclared('Variable', node.name)

        """
        Checking type of RHS value:
            value: 'Expr' -> BinaryOp, UnaryOp, FunctionCall, ArrayAccess, ArrayLiteral, Identifier
        """

        type_ = self.visit(node.value, param)
        if not isinstance(node.value, FunctionCall) and isinstance(type_,FunctionType):
            if isinstance(node.value, Identifier):
                raise Undeclared(IdentifierMarker(), node.value.name)

        if node.type_annotation:
            if type_:
                if not self.type_compatible(node.type_annotation, type_):
                    raise TypeMismatchInStatement(node)
            else:
                if isinstance(node.type_annotation, ArrayType):
                    if not int(str(node.type_annotation.size)) == 0:
                        raise TypeMismatchInStatement(node)
            type_ = node.type_annotation
            
        if not type_:
            raise TypeCannotBeInferred(node)

        return Symbol(node.name, type_)


    def visit_while_stmt(self, node: 'WhileStmt', param: List[List['Symbol']]):
        self.number_loop += 1
        condition_type = self.visit(node.condition, param)
        if not isinstance(condition_type, BoolType):
            raise TypeMismatchInStatement(node)
        self.visit(node.body, param)
        self.number_loop -= 1
    

    def visit_for_stmt(self, node: 'ForStmt', param: List[List['Symbol']]):
        """
        ForStmt({self.variable}, {self.iterable}, {self.body})
        for(a in 1)
        ForStmt({a}, {self.iterable}, {self.body})
        """
        # In loop
        self.number_loop += 1
        var_name = node.variable
        collection = self.visit(node.iterable, param) 
        
        if not isinstance(collection, ArrayType):
            raise TypeMismatchInStatement(node)

        if not self.isFor:
            self.isFor = True

        # Visit body with loop variable in new scope
        self.visit(node.body, [[Symbol(var_name, collection.element_type)]] + param)
        
        if self.isFor:
            self.isFor = False
        # Out loop
        self.number_loop -= 1
    

    def visit_break_stmt(self, node: 'BreakStmt', param: List[List['Symbol']]):
        if self.number_loop == 0:
            raise MustInLoop(node)
        return 


    def visit_continue_stmt(self, node: 'ContinueStmt', param: List[List['Symbol']]):
        if self.number_loop == 0: 
            raise MustInLoop(node)
        return 


    def visit_assignment(self, node: 'Assignment', param: List[List['Symbol']]):
        try:
            lhs = self.visit(node.lvalue, param)

            # Check constanst variable
            def is_const(node, param):
                temp = node
                while not isinstance(temp, (IdLValue, Identifier)):
                    temp = temp.array
                res: Optional['Symbol'] = next(filter(None, map(lambda item_list: self.lookup(temp.name, item_list, lambda x: x.name), param)), None)
                return res and res.isConst
            if is_const(node.lvalue, param):
                raise TypeMismatchInStatement(node)
        except TypeMismatchInStatement:
            raise TypeMismatchInStatement(node)
            
        rhs = self.visit(node.value, param)
        if lhs and rhs:
            if not self.type_compatible(lhs, rhs):
                raise TypeMismatchInStatement(node)


    def visit_block_stmt(self, node: 'BlockStmt', param: List[List['Symbol']]):
        reduce(lambda acc, ele: [([result] + acc[0]) if isinstance(result := self.visit(ele, acc), Symbol) else acc[0]] + acc[1:], 
            node.statements, param if self.isFor else [[]] + param 
            )
    

    def visit_id_lvalue(self, node: 'IdLValue', param: List[List['Symbol']]):
        id_lvalue_symbol: Optional['Symbol'] = next(filter(
                                                        lambda x: x is not None and not isinstance(x.typ, FunctionType), 
                                                        (self.lookup(node.name, scope, lambda x: x.name) for scope in param)
                                                    ), None)
        if not id_lvalue_symbol:
            raise Undeclared(IdentifierMarker(), node.name)
        return id_lvalue_symbol.typ # typ: Identifier | ArrayAccessLValue
    

    def visit_identifier(self, node: 'Identifier', param: List[List['Symbol']]):
        # Traverse from current scope to global scope
        id_symbol: Optional['Symbol'] = next(
            filter(None, (self.lookup(node.name, scope, lambda x: x.name) for scope in param)),
            None 
        )
        if not id_symbol:
            raise Undeclared(IdentifierMarker(), node.name)

        return id_symbol.typ  


    def visit_function_call(self, node: 'FunctionCall', param: List[List['Symbol']]):
        def raise_error():
            if not self.in_expr_stmt:
                raise TypeMismatchInExpression(node)
            raise TypeMismatchInStatement(node)

        if isinstance(node.function, Identifier):
            # Traverse from current scope to global scope
            func_symbol = next(
                filter(None, (self.lookup(node.function.name, scope, lambda x: x.name) for scope in param)),
                None
            )
            
            # function not found in symbol table
            if not func_symbol or not isinstance(func_symbol.typ, FunctionType):
                raise Undeclared(FunctionMarker(), node.function.name)
            
            # Check len of args
            if len(func_symbol.typ.param_types) != len(node.args):
                raise_error()

            # Symbol("len", FunctionType([ArrayType(IntType(), -1)], IntType()))
            if(func_symbol.name == "len"):
                if type(func_symbol.typ.param_types[0]) != type(self.visit(node.args[0], param)):
                    raise_error()
                return func_symbol.typ.return_type

            # Check compatiple param type
            if func_symbol.typ.param_types:
                if not all(self.type_compatible(param_type, self.visit(arg, param))
                        for arg, param_type in zip(node.args, func_symbol.typ.param_types)):
                    raise_error()
            
            # Return Void in statement
            if not self.in_expr_stmt and isinstance(func_symbol.typ.return_type, VoidType):
                raise_error()
    
            return func_symbol.typ.return_type          # Return type of function type
        else: 
            raise_error()


    def visit_if_stmt(self, node: 'IfStmt', param: List[List['Symbol']]): 
        condition_type = self.visit(node.condition, param)
        if not isinstance(condition_type, BoolType):
            raise TypeMismatchInStatement(node)
        self.visit(node.then_stmt, param)
        if node.elif_branches:
            def elif_proceess(elif_stmt: tuple):
                expr_type, block_stmt = elif_stmt
                if not isinstance(self.visit(expr_type, param), BoolType):
                    raise TypeMismatchInStatement(node)
                self.visit(block_stmt, param)

            list(map(elif_proceess, node.elif_branches))
        if node.else_stmt:
            self.visit(node.else_stmt, param)
    

    def visit_return_stmt(self, node: 'ReturnStmt', param: List[List['Symbol']]): 
        if node.value:
            if self.current_function is not None and not type(self.visit(node.value, param)) == type(self.current_function.return_type):
                raise TypeMismatchInStatement(node)


    def visit_expr_stmt(self, node: 'ExprStmt', param: List[List['Symbol']]): 
        self.in_expr_stmt = True
        # Check functioncall
        try:
            expr_type = self.visit(node.expr, param) 
            if not isinstance(expr_type, VoidType):
                if isinstance(node.expr, FunctionCall):
                    raise TypeMismatchInStatement(node)
                elif isinstance(node.expr, BinaryOp):
                    binary_op = node.expr
                    if binary_op.operator == ">>":
                        raise TypeMismatchInStatement(node)

            if self.in_expr_stmt:
                self.in_expr_stmt = False
        except TypeMismatchInStatement:
            raise TypeMismatchInStatement(node)


    def visit_binary_op(self, node: 'BinaryOp', param: List[List['Symbol']]): 
        """
            self.left = left
            self.operator = operator  # '+', '-', '*', '/', '%', '==', '!=', '<', '<=', '>', '>=', '&&', '||', '>>'
            self.right = right
        """
        op_type = node.operator
        left_type = self.visit(node.left, param)

        # Check if op is pipeline
        if op_type == ">>":
            if isinstance(node.right, Identifier):
                pipeline_call = FunctionCall(node.right, [node.left])
                try:
                    return self.visit(pipeline_call, param)
                except Undeclared:
                    raise Undeclared(FunctionMarker(), node.right.name)
                except TypeMismatchInStatement:
                    raise TypeMismatchInStatement(node)
                except TypeMismatchInExpression:
                    raise TypeMismatchInExpression(node)
            elif isinstance(node.right, FunctionCall):
                pipeline_call = FunctionCall(node.right.function, [node.left] + node.right.args)
                try:
                    return self.visit(pipeline_call, param)
                except Undeclared:
                    if isinstance(pipeline_call.function, Identifier):
                        raise Undeclared(FunctionMarker(), pipeline_call.function.name)
                    else:
                        raise TypeMismatchInExpression(node)
                except TypeMismatchInStatement:
                    raise TypeMismatchInStatement(node)
                except TypeMismatchInExpression:
                    raise TypeMismatchInExpression(node)
            else:
                raise TypeMismatchInExpression(node)

        right_type = self.visit(node.right, param)

        if left_type is not None and right_type is not None:
            if op_type in ["+", "-", "*", "/", "%"]:
                if op_type == "%":
                    if not (isinstance(left_type, IntType) and isinstance(right_type, IntType)):
                        raise TypeMismatchInExpression(node)
                    else:
                        return IntType()
                if op_type == "+" and isinstance(left_type, StringType) and isinstance(right_type, (IntType, FloatType, BoolType, StringType)):
                    return StringType()
                elif isinstance(left_type, IntType) and isinstance(right_type, IntType):
                    return IntType()
                elif isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
                    return FloatType()
                else:
                    raise TypeMismatchInExpression(node)
            elif op_type in ["<", "<=", ">", ">="]:
                if isinstance(left_type, (IntType, FloatType)) or isinstance(right_type, (IntType, FloatType)):
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(node)
            elif op_type in ["==", "!="]:
                if (isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))) \
                                    or (isinstance(left_type, StringType) and isinstance(right_type, StringType)) \
                                    or (isinstance(left_type, BoolType) and isinstance(right_type, BoolType)):
                    return BoolType()
                else: 
                    raise TypeMismatchInExpression(node)
            elif op_type in ["&&", "||"]:
                if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(node)
            else:
                raise TypeMismatchInExpression(node)
        else: 
            raise TypeMismatchInExpression(node)
        

    def visit_unary_op(self, node: 'UnaryOp', param: List[List['Symbol']]): 
        operand_type = self.visit(node.operand, param)
        op_type = node.operator
        if op_type in ["+", "-"]:
            if isinstance(operand_type, (FloatType, IntType)):
                return operand_type
            raise TypeMismatchInExpression(node)
        elif op_type in ["!"]:
            if isinstance(operand_type, BoolType):
                return operand_type
            raise TypeMismatchInExpression(node)


    def visit_array_access(self, node: 'ArrayAccess', param: List[List['Symbol']]): 
        type_array = self.visit(node.array, param)
        type_index = self.visit(node.index, param)

        if not isinstance(type_array, ArrayType):
            raise TypeMismatchInExpression(node)
        if not isinstance(type_index, IntType):
            raise TypeMismatchInExpression(node)
        return type_array.element_type


    def visit_array_literal(self, node: 'ArrayLiteral', param: List[List['Symbol']]): 
        list_elements = node.elements
    
        # Check all types in arrayliteral
        if list_elements and (first_type := self.visit(list_elements[0], param)):
            if not all(
                    type(self.visit(elem, param)) == type(first_type)
                    for elem in list_elements[1:]):
                raise TypeMismatchInExpression(node)

            return ArrayType(first_type, len(list_elements)) 
        return None


    def visit_array_access_lvalue(self, node: 'ArrayAccessLValue', param: List[List['Symbol']]): 
        type_array = self.visit(node.array, param)
        type_index = self.visit(node.index, param)

        if not isinstance(type_array, ArrayType):
            raise TypeMismatchInExpression(node)
        
        if not isinstance(type_index, IntType):
            raise TypeMismatchInExpression(node)

        return type_array.element_type


    # Literals
    def visit_integer_literal(self, node: 'IntegerLiteral', param): return IntType()
    def visit_float_literal(self, node: 'FloatLiteral', param): return FloatType()
    def visit_boolean_literal(self, node: 'BooleanLiteral', param): return BoolType()
    def visit_string_literal(self, node: 'StringLiteral', param): return StringType()
    def visit_int_type(self, node: 'IntType', param): return node
    def visit_float_type(self, node: 'FloatType', param): return node
    def visit_bool_type(self, node: 'BoolType', param): return node
    def visit_string_type(self, node: 'StringType', param): return node
    def visit_void_type(self, node: 'VoidType', param): return node
    def visit_array_type(self, node: 'ArrayType', param): return node
    