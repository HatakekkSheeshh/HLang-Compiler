"""
Code Generator for CS programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "CS"
        self.emit: Emitter = Emitter(self.class_name + ".j")
        self.frame: Frame = None

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))

        ## Main
        self.frame = Frame("main")
        self.emit.print_out(self.emit.emit_method(lexeme="main",in_type="([Ljava/lang/String;)V", is_static=True))
        self.frame.enter_scope()
        self.frame.get_new_index()
        
        reduce(lambda acc, cur: self.visit(cur, acc),node.stmts, {})

        self.emit.print_out(self.emit.emit_return())
        self.emit.print_out(self.emit.emit_end_method(self.frame))
        self.frame.exit_scope()

        ## Contructor
        frame = Frame("<init>")
        self.emit.print_out(self.emit.emit_method(lexeme="<init>",in_type="()V", is_static=False))
        frame.enter_scope()
        self.emit.print_out(self.emit.emit_read_var("this", frame.get_new_index(), frame ))
        self.emit.print_out(self.emit.emit_invoke_special(frame))

        self.emit.print_out(self.emit.emit_return())
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()

        self.emit.emit_epilog()

    def visit_const_decl(self, node: "ConstStmt", o: dict = None):
        idx = self.frame.get_new_index()
        o[node.name] = idx

        self.emit.print_out(self.visit(node.value, o))
        self.emit.print_out(self.emit.emit_write_var(idx, self.frame))
        return o

    def visit_call_stmt(self, node: "CallStmt", o: dict = None):
        self.emit.print_out(self.visit(node.args, o))
        self.emit.print_out(self.emit.emit_invoke_static("io/" + node.function_name, "(I)V", self.frame))
        return o

    def visit_binary_op(self, node: "BinaryOp", o: dict = None):
        return self.visit(node.left, o) + self.visit(node.right, o) + self.emit.emit_add_op(self.frame)

    def visit_identifier(self, node: "Identifier", o: dict = None):
        index = o[node.name]
        return self.emit.emit_read_var(IntType(), index, self.frame)

    def visit_integer_literal(self, node: "IntegerLiteral", o: dict = None):
        return self.emit.emit_push_iconst(node.value, self.frame)

    def visit_int_type(self, node: "IntType", o: dict = None):
        pass