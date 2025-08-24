"""
Static Semantic Checker for CS Programming Language
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .static_error import Redeclared, Undeclared
  
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker


class StaticChecker(ASTVisitor):
    def __init__(self):
        self.env = set()
        self.env.add("print")

    def check_program(self, ast):
        self.visit(ast)

    def visit_program(self, node: "Program", o: Any = None):
        for stmt in node.stmts:
            self.visit(stmt, self.env)

    def visit_const_decl(self, node: "ConstStmt", o: Any = None):
        if node.name in o:
            raise Redeclared(node.name)
        o.add(node.name)
        if node.value:
            self.visit(node.value, o)

    def visit_call_stmt(self, node: "CallStmt", o: Any = None):
        if node.function_name not in o:
            raise Undeclared(FunctionMarker(), node.function_name)
        self.visit(node.args, o)

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        self.visit(node.left, o)
        self.visit(node.right, o)

    def visit_identifier(self, node: "Identifier", o: Any = None):
        if node.name not in o:
            raise Undeclared(IdentifierMarker(), node.name)

    def visit_integer_literal(self, node: "IntegerLiteral", o: Any = None):
        pass

    def visit_int_type(self, node: "IntType", o: Any = None):
        pass