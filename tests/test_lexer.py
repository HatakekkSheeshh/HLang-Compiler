from utils import Tokenizer

## python3 -m pytest -v --timeout=3 tests/test_lexer.py
def test_001():
    """Test identifier"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_002():
    """Test KEYWORDS"""
    source = "const int"
    expected = "const,int,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_003():
    """Test OPERATORS and SEPARATOR"""
    source = "+ = () ;"
    expected = "+,=,(,),;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004():
    """Test INT_LIT"""
    source = "123"
    expected = "123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    """Test COMMENT"""
    source = "// VO TIEN 10. PPL"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    """Test ERROR"""
    source = "#"
    expected = "Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected