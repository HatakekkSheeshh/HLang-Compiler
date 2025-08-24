from utils import ASTGenerator
from src.utils.nodes import *

## python3 -m pytest -v --timeout=3 tests/test_ast_gen.py
def test_001():
    """Test basic"""
    source = "const x int = 42;"
    expected = Program([ConstStmt("x", IntType(), IntegerLiteral(42))])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_002():
    """Test Full"""
    source = """
        const a = 1;
        const b int = 2;
        print(a);
        print(b + 2);
"""
    expected = Program([
            ConstStmt("a", None, IntegerLiteral(1)), 
            ConstStmt("b", IntType(), IntegerLiteral(2)), 
            CallStmt("print", Identifier("a")), 
            CallStmt("print", BinaryOp(Identifier("b"), "+", IntegerLiteral(2)))
        ])
    assert str(ASTGenerator(source).generate()) == str(expected)
