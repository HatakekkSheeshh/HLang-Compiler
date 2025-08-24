from src.utils.nodes import *
from utils import CodeGenerator

## python3 -m pytest -v --timeout=3 tests/test_codegen.py
def test_001():
    source = """
print(1);
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_002():
    source = """
print(1 + 100 + 2);
"""
    expected = "103"
    assert CodeGenerator().generate_and_run(source) == expected

def test_003():
    source = """
const a = 2;
print(a);
"""
    expected = "2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_004():
    source = """
const a = 2;
const b = 3 + a;
print(a + b);
"""
    expected = "7"
    assert CodeGenerator().generate_and_run(source) == expected


