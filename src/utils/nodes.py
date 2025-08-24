"""
AST Node classes for CS programming language.
This module defines all the AST node types used to represent
the abstract syntax tree for CS programs.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .visitor import ASTVisitor


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    def __init__(self):
        self.line = None
        self.column = None
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor'):
        """Accept a visitor for the Visitor pattern."""
        pass
    
    def __str__(self):
        """Default string representation."""
        return f"{self.__class__.__name__}()"


# ============================================================================
# Program and Top-level Declarations
# ============================================================================
@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    stmts: List['Stmt']
    
    def accept(self, visitor, param):
        return visitor.visit_program(self, param)
    
    def __str__(self):
        return f"Program([{', '.join(str(stmt) for stmt in self.stmts)}])"
            

# ============================================================================
# Type System
# ============================================================================
@dataclass
class Type(ASTNode):
    """Base class for type annotations."""
    pass

@dataclass
class IntType(Type):
    """Integer type node."""
    
    def accept(self, visitor, param):
        return visitor.visit_int_type(self, param)
    
    def __str__(self):
        return "IntType()"


# ============================================================================
# Statements
# ============================================================================
@dataclass
class Stmt(ASTNode):
    """Base class for all statement nodes."""
    pass

@dataclass
class ConstStmt(Stmt):
    """Constant statement."""
    name: str
    type_annotation: Optional[Type]
    value: 'Expr'
    
    def accept(self, visitor, param):
        return visitor.visit_const_decl(self, param)
    
    def __str__(self):
        type_str = f", {self.type_annotation}" if self.type_annotation else ", None"
        return f"ConstStmt(\"{self.name}\"{type_str}, {self.value})"


@dataclass
class CallStmt(Stmt):
    """Call statement."""
    function_name: str
    args: 'Expr'
    
    def accept(self, visitor, param):
        return visitor.visit_call_stmt(self, param)
    
    def __str__(self):
        return f"CallStmt(\"{self.function_name}\", {self.args})"


# ============================================================================
# Expressions
# ============================================================================
@dataclass
class Expr(ASTNode):
    """Base class for all expression nodes."""
    pass

@dataclass
class BinaryOp(Expr):
    """Binary operation expression."""
    left: Expr
    operator: str
    right: Expr

    def accept(self, visitor, param):
        return visitor.visit_binary_op(self, param)
    
    def __str__(self):
        return f"BinaryOp({self.left}, \"{self.operator}\", {self.right})"

@dataclass
class Identifier(Expr):
    """Identifier expression."""
    name: str
    
    def accept(self, visitor, param):
        return visitor.visit_identifier(self, param)
    
    def __str__(self):
        return f"Identifier(\"{self.name}\")"


# ============================================================================
# Literal Expressions
# ============================================================================
@dataclass
class Literal(Expr):
    """Base class for literal expressions."""
    pass

@dataclass
class IntegerLiteral(Literal):
    """Integer literal expression."""
    value: int
    
    def accept(self, visitor, param):
        return visitor.visit_integer_literal(self, param)
    
    def __str__(self):
        return f"IntegerLiteral({self.value})"
