"""
Static Error Classes for CS Semantic Analysis
This module defines all the exception classes that can be raised during static semantic checking.
"""

class StaticError(Exception):
    """Base class for all static semantic errors"""
    pass


class Redeclared(StaticError):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Redeclared: {name}")


class Undeclared(StaticError):
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name
        super().__init__(f"Undeclared {str(kind)}: {name}")


# Helper classes for Undeclared error
class Identifier:
    """Marker class to indicate undeclared identifier (variable/constant)"""
    def __str__(self):
        return "Identifier"


class Function:
    """Marker class to indicate undeclared function"""
    def __str__(self):
        return "Function"
