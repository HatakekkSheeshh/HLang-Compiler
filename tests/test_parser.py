from utils import Parser

## python3 -m pytest -v --timeout=3 tests/test_parser.py
def test_001():
    """Test Success"""
    source = """
        const a = 1;
        const b int = 2;
        print(a);
        print(b + 2);
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    """Test Const"""
    source = """
        const a = ;
"""
    expected = "Error on line 2 col 18: ;"
    assert Parser(source).parse() == expected

def test_003():
    """Test Call"""
    source = """
        print(c)
"""
    expected = "Error on line 3 col 0: <EOF>"
    assert Parser(source).parse() == expected