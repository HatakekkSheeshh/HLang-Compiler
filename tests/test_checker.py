from utils import Checker

## python3 -m pytest -v --timeout=3 tests/test_checker.py
def test_001():
    source = """
    const a = 1;
    const a = 2;
"""
    expected = "Redeclared: a"
    assert Checker(source).check_from_source() == str(expected)

def test_002():
    source = """
    const a = 1;
    const b = 2 + a;
    const c = 3 + d;
"""
    expected = "Undeclared Identifier: d"
    assert Checker(source).check_from_source() == str(expected)

def test_003():
    source = """
    const a = 1;
    print(a);
    print(b);
"""
    expected = "Undeclared Identifier: b"
    assert Checker(source).check_from_source() == str(expected)

def test_004():
    source = """
    const a = 1;
    foo(a);
"""
    expected = "Undeclared Function: foo"
    assert Checker(source).check_from_source() == str(expected)
