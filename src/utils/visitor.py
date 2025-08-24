"""
Visitor interface for AST traversal in CS programming language.
This module defines the abstract visitor pattern interface for traversing
and processing AST nodes.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .nodes import *


class ASTVisitor(ABC):
    """Abstract base class for AST visitors."""


    def visit(self, node: "ASTNode", o: Any = None):
        """Dispatch visit to the correct method based on node type."""
        return node.accept(self, o)

    # =========================================================================
    # Program and declarations
    # =========================================================================
    @abstractmethod
    def visit_program(self, node: "Program", o: Any = None):
        pass

    # =========================================================================
    # Statements
    # =========================================================================
    @abstractmethod
    def visit_const_decl(self, node: "ConstStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_call_stmt(self, node: "CallStmt", o: Any = None):
        pass
    
    # =========================================================================
    # Types
    # =========================================================================
    @abstractmethod
    def visit_int_type(self, node: "IntType", o: Any = None):
        pass

    # =========================================================================
    # Expressions
    # =========================================================================
    @abstractmethod
    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        pass

    @abstractmethod
    def visit_identifier(self, node: "Identifier", o: Any = None):
        pass

    # =========================================================================
    # Literals
    # =========================================================================
    @abstractmethod
    def visit_integer_literal(self, node: "IntegerLiteral", o: Any = None):
        pass