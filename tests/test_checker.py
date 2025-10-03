from utils import Checker

# Adjust
from utils import ASTGenerator 
from src.semantics.static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)
from src.utils.nodes import *

def test_000():
    source = """
func main() -> int {
    return 1;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_001():
    source = """
func hello() -> void {
    let x: int = 5;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_002():
    source = """
func main() -> void {
    let x: int = 5;
    let x: int = 10;
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected


def test_003():
    source = """
const x: int = 5;
const x: int = 10;
func main() -> void {

}
"""
    expected = "Redeclared Constant: x"
    assert Checker(source).check_from_source() == expected


def test_004():
    source = """
func main() -> void {}
func main() -> void {}
"""
    expected = "Redeclared Function: main"
    assert Checker(source).check_from_source() == expected


def test_005():
    source = """
func main() -> void {
    let x = y;
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected


def test_006():
    source = """
func foo() -> void {}
func main() -> void {
    foo();
    goo();
}
"""
    expected = "Undeclared Function: goo"
    assert Checker(source).check_from_source() == expected


def test_007():
    source = """
func main() -> void {
    let x = input();
    let y = input1();
}
"""
    expected = "Undeclared Function: input1"
    print(str(ASTGenerator(source).generate()))
    assert Checker(source).check_from_source() == expected
 

def test_008():
    source = """
func main() -> void {
    break;
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


def test_009():
    """Test a valid program that should pass all checks"""
    source = """
const PI: float = 3.14;
func main() -> void {
    let x: int = 5;
    let y = x + 1;
}
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected


def test_010():
    """Test redeclared variable error"""
    source = """
func main() -> void {
    let x: int = 5;
    let x: int = 10;
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected


def test_011():
    """Test undeclared identifier error"""
    source = """
func main() -> void {
    let x = y + 1;
}
"""
    expected = "Undeclared Identifier: y"
    print(ASTGenerator(source).generate())
    assert Checker(source).check_from_source() == expected


def test_012():
    """Test type mismatch error"""
    source = """
func main() -> void {
    let x: int = "hello";
}
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected


def test_013():
    """Test no main function error"""
    source = """
func hello() -> void {
    let x: int = 5;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_014():
    """Test break not in loop error"""
    source = """
func main() -> void {
    break;
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


def test_015():
    source = """
    const a = 1;
    func goo(a: int, b: string) -> void {}
    func foo(c: int, b: string, c: float) -> void {}
    func main() -> void {}
    """
    expected = "Redeclared Parameter: c"
    assert Checker(source).check_from_source() == expected
    

def test_016():
    source = """
    const a = 1;
    func main() -> void {
        let a = 1;
        let b = 1;
        {
            let a = 2;
            let a = 1;
        }
    }
    """
    expected = "Redeclared Variable: a"
    assert Checker(source).check_from_source() == expected


def test_017():
    source = """
    func main() -> void {
        a = 1;
    }
    """
    expected = "Undeclared Identifier: a"
    print(ASTGenerator(source).generate())
    assert Checker(source).check_from_source() == expected
    

def test_018():
    source = """
    const foo = 1;
    func main() -> void {
        foo();
    }
    """
    expected = "Undeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_019():
    source = """
    const foo = 1;
    func main() -> void {
        let foo = 1 ;
        foo() ;
    }
    """
    expected = "Undeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_020():
    source = """
    func main() -> void {
        let a = str2int("777");
    }
    """
    expected = "Static checking passed"
    print(ASTGenerator(source).generate())
    assert Checker(source).check_from_source() == expected


def test_021():
    source = """
    func one() -> int {return 1;}
    func main() -> void {
        let a = one()[1] ;
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccess(FunctionCall(Identifier(one), []), IntegerLiteral(1))"
    print(ASTGenerator(source).generate())
    assert Checker(source).check_from_source() == expected


# TEST CASE
def test_022():
    source = """
func main() -> void {
    let a: int = [1,2,3];
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", IntType(), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])))
    assert Checker(source).check_from_source() == str(expected)

def test_023():
    source = """
func main() -> void {
    let a: [int; 3] = [1,2,"s"];
}
"""
    expected = TypeMismatchInExpression(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), StringLiteral('s')]))
    print((ASTGenerator(source).generate()))
    assert Checker(source).check_from_source() == str(expected)

def test_024():
    source = """
func main() -> void {
    for (a in 1) {}
}
"""
    expected = TypeMismatchInStatement(ForStmt("a", IntegerLiteral(1), BlockStmt([])))
    assert Checker(source).check_from_source() == str(expected)

def test_025():
    source = """
func main() -> void {
    return [1,2];
}
"""
    expected = TypeMismatchInStatement(ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])))
    assert Checker(source).check_from_source() == str(expected)

def test_026():
    source = """
func main() -> void {
    let a = [1,2,3];
    let b = a[2][3];
}
"""
    expected = TypeMismatchInExpression(ArrayAccess(ArrayAccess(Identifier("a"), IntegerLiteral(2)), IntegerLiteral(3)))
    print(str(ASTGenerator(source).generate()))
    assert Checker(source).check_from_source() == str(expected)


def test_027():
    source = """
func main() -> void {
    print("s");
    input();
}
"""
    expected = TypeMismatchInStatement(ExprStmt(FunctionCall(Identifier("input"), [])))
    assert Checker(source).check_from_source() == str(expected)

def test_028():
    source = """
func main() -> void {
    let a: int = int2str(1) >= float2str(1.0);
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(FunctionCall(Identifier(int2str), [IntegerLiteral(1)]), >=, FunctionCall(Identifier(float2str), [FloatLiteral(1.0)]))"
    assert Checker(source).check_from_source() == str(expected)

def test_029():
    source = """
func main() -> void {
    let a: int = int2str();
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("int2str"), []))
    assert Checker(source).check_from_source() == str(expected)

def test_030():
    source = """
func HIEU(a:int) -> void{
    a = 1;
}
func main() -> void {}
"""
    expected =  TypeMismatchInStatement(Assignment(IdLValue("a"), IntegerLiteral(1)))
    assert Checker(source).check_from_source() == str(expected)

def test_031():
    source = """
func main() -> void {
    let a = [1, 2];
    a[1+0] = 1;
    a = [1,2,3];
}
"""
    expected = TypeMismatchInStatement(Assignment(IdLValue("a"), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])))
    assert Checker(source).check_from_source() == str(expected)

def test_032():
    source = """
func main() -> void {
    let a = --1 > 2 && true;
    let b = "s" + 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)


def test_033():
    source = """
func main() -> void {
    let a = [1,2,3];
    let b = a[2];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_034():
    source = """
const a = 5;
func main() -> void {
    a = 6;
}
"""
    expected = TypeMismatchInStatement(Assignment(IdLValue("a"), IntegerLiteral(6)))
    assert Checker(source).check_from_source() == str(expected)

def test_035():
    source = """
func main() -> void {
    main();
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_036():
    source = """
func main() -> void {
    if(1+1){}
}
"""
    expected = TypeMismatchInStatement(
    IfStmt(condition=BinaryOp(left=IntegerLiteral(1), operator="+", right=IntegerLiteral(1)),then_stmt=BlockStmt([]), elif_branches=[], else_stmt=None))
    print(str(ASTGenerator(source).generate()))
    assert Checker(source).check_from_source() == str(expected)

def test_037():
    source = """
func main() -> void {
    if(true){
    
    }
    else if(1+1){
    
    }
    else {
    
    }
}
"""
    expected = TypeMismatchInStatement(
        IfStmt(
            condition=BooleanLiteral(True), 
            then_stmt=BlockStmt([]), 
            elif_branches=[(BinaryOp(left=IntegerLiteral(1), operator="+", right=IntegerLiteral(1)), BlockStmt([]))], 
            else_stmt=BlockStmt([])
        )
    )
    print(str(ASTGenerator(source).generate()))
    assert Checker(source).check_from_source() == str(expected)


def test_038():
    source = """
const a = 1;
const b = a;
const c = d;
func main() -> void {}
"""
    expected = "Undeclared Identifier: d"
    assert Checker(source).check_from_source() == str(expected)


def test_039():
    source = """
const array = [[1], [2]];
func main() -> void {
    for (a in array) {
        a = [2];
        a = [1,2];
    }
}
"""
    expected = TypeMismatchInStatement(Assignment(IdLValue("a"), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])))
    assert Checker(source).check_from_source() == str(expected)


def test_040():
    source = """
const array = [1,2,3];
func main() -> void {
    for (a in array) {
        a = 2;
        let a = "string";
    }
}
"""
    expected = "Redeclared Variable: a"
    assert Checker(source).check_from_source() == str(expected)


def test_041():
    source = """
const a = 1;
func main() -> void {
    let a = 1;
    let b = 1;
    {
        let a = 2;
    }
    let b = 1;
}
"""
    expected = "Redeclared Variable: b"
    assert Checker(source).check_from_source() == str(expected)


def test_042():
    source = """
func main() -> void {
    let i = true;
    while(i) {
        let i = "string";
        i = false;
    }
}
"""
    expected = TypeMismatchInStatement(Assignment(IdLValue("i"), BooleanLiteral(False)))
    assert Checker(source).check_from_source() == str(expected)


def test_043():
    source = """
func foo() -> int {return 1;}
func main() -> void {
    let a = foo;
}
"""
    expected = "Undeclared Identifier: foo"
    assert Checker(source).check_from_source() == str(expected)


def test_044():
    source = """
func foo() -> int {return 1;}
func main() -> void {
    foo = 1;
}
"""
    expected = "Undeclared Identifier: foo"
    assert Checker(source).check_from_source() == str(expected)


def test_045():
    source = """
func main() -> void {
    let a: int = 1 % 2.0;
}
"""
    expected = TypeMismatchInExpression(BinaryOp(IntegerLiteral(1), "%", FloatLiteral(2.0)))
    assert Checker(source).check_from_source() == str(expected)


def test_046():
    source = """
func main() -> void {
    let a: bool = 1 == 1;
    let b: bool = 1.0 != 1.0;
    let c: bool = 1 == 1.0;
    let d: bool = 1.0 != 1;
    let e: bool = "a" != "b";
    let f: bool = true == false;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)


def test_047():
    source = """
func main() -> void {
    let a: bool = 1 >= 1;
    let b: bool = 1.0 <= 1.0;
    let c: bool = 1 > 1.0;
    let d: bool = 1.0 < 1;
    let e: bool = "a" <= "b";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('a'), <=, StringLiteral('b'))"
    assert Checker(source).check_from_source() == str(expected)


def test_048():
    source = """
func main() -> void {
    let a: [int; 1] = [];
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", ArrayType(IntType(), 1), ArrayLiteral([])))
    assert Checker(source).check_from_source() == str(expected)


def test_049():
    source = """
func main() -> void {
    let a: string = input(1);
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("input"), [IntegerLiteral(1)]))
    assert Checker(source).check_from_source() == str(expected)


def test_050():
    source = """
func HIEU() -> int {return 1;}
func HIEU1(a: int, b: string) -> int {return 1;}
func HIEU2(a: int) -> int {return 1;}
func main() -> void {
    let a: int = HIEU() + HIEU1(1, "s") + HIEU2(3);
    let b: int = HIEU2(1.0);
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("HIEU2"), [FloatLiteral(1.0)]))
    assert Checker(source).check_from_source() == str(expected)


def test_051():
    source = """
func HIEU() -> void {}
func main() -> void {
    let b = HIEU();
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("HIEU"), []))
    assert Checker(source).check_from_source() == str(expected)


def test_052():
    source = """
func TIEN() -> void {}
func main() -> void {
    print("a");
    print(1);
}
"""
    expected = TypeMismatchInStatement(ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(1)])))
    assert Checker(source).check_from_source() == str(expected)


def test_053():
    source = """
func HIEU(a: int) -> void {}
func main() -> void {
    HIEU(1);
    HIEU(1.2);
}
"""
    expected = TypeMismatchInStatement(ExprStmt(FunctionCall(Identifier("HIEU"), [FloatLiteral(1.2)])))
    assert Checker(source).check_from_source() == str(expected)


def test_054():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}

func main() -> void {
    let a: int = 1 >> C;
}
"""
    expected = "Undeclared Function: C"
    print(str(ASTGenerator(source).generate()))
    assert Checker(source).check_from_source() == str(expected)


def test_055():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}

func main() -> void {
    let a: int = "s" >> A;
}
"""
    expected = TypeMismatchInExpression(BinaryOp(StringLiteral('s'), ">>", Identifier("A")))
    assert Checker(source).check_from_source() == str(expected)


def test_056():
    source = """
func A(a: int) -> int {return 1;}
func B() -> int {return 1;}

func main() -> void {
    let a: string = 1 >> int2str;
    let b: string = 1.0 >> float2str;
    let c: string = true >> bool2str;
    let d: string = "1" >> print;
}
"""
    expected = TypeMismatchInExpression(BinaryOp(StringLiteral('1'), ">>", Identifier("print")))
    assert Checker(source).check_from_source() == str(expected)


def test_057():
    source = """
func TIEN(a: int) -> int {return 1;}
func main() -> void {
    2 >> TIEN;
}
"""
    expected = TypeMismatchInStatement(ExprStmt(BinaryOp(IntegerLiteral(2), ">>", Identifier("TIEN"))))
    assert Checker(source).check_from_source() == str(expected)


def test_058():
    source = """
func main() -> void {
    1 + "A";
}
"""
    expected = TypeMismatchInExpression(BinaryOp(IntegerLiteral(1), "+", StringLiteral('A')))
    assert Checker(source).check_from_source() == str(expected)


def test_059():
    source = """
func A(a: int, b: int) -> void {return ;}
func B(a: int) -> int {return 1;}

func main() -> void {
    2 >> B >> A(2);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)


def test_060():
    source = """
const a: [int; 3] = [1,2,3];
func main() -> void {
    let i = a[1];
    a[1] = 1; // const
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(1)), IntegerLiteral(1))"
    assert Checker(source).check_from_source() == str(expected)


def test_061():
    source = """
func main() -> void {
    let arr =  [];
}
"""
    print(str(ASTGenerator(source).generate()))
    expected = TypeCannotBeInferred(VarDecl(name = "arr", type_annotation = None, value = ArrayLiteral([])))
    assert Checker(source).check_from_source() == str(expected)


def test_062():
    source = """
const arr = [1,2,3];
func main() -> void {
    arr[1] = 2;
}
"""
    print(str(ASTGenerator(source).generate()))
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(2))"
    assert Checker(source).check_from_source() == str(expected)


def test_063():
    source = """
const arr = [1,2,3];
func main() -> void {
    arr = [2];
}
"""
    print(str(ASTGenerator(source).generate()))
    expected = "Type Mismatch In Statement: Assignment(IdLValue(arr), ArrayLiteral([IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == str(expected)


def test_064():
    source = """
// Valid: Forward reference to global function
func validCall() -> void {
    globalFunc();  // Valid: globalFunc declared later but in global scope
}

func globalFunc() -> void {
    print("Global function");
}

func main() -> void {
    validCall();
}
"""
    print(str(ASTGenerator(source).generate()))
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)


def test_065():
    source = """
const arr = [1,2,3];
func main() -> void {
    let a: int = len(arr);
}
"""
    print(str(ASTGenerator(source).generate()))
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)


def test_066():
    source = """
const int2str = 1;
func main() -> void {}
"""
    expected = "Redeclared Constant: int2str"
    assert Checker(source).check_from_source() == str(expected)


def test_067():
    source = """
const main = 1;
func main() -> void {}
"""
    expected = "Redeclared Function: main"
    assert Checker(source).check_from_source() == str(expected)


def test_068():
    source = """
const a = goo();
func foo() -> void {}
func goo() -> int {return 1;}
func main() -> void {}
"""
    expected = "Undeclared Function: goo"
    assert Checker(source).check_from_source() == str(expected)


def test_069():
    source = """
const a: [int; 0] = [];
func main() -> void {}
"""
    expected = 'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_070():
    source = """
func main() -> void {
    let a: [int; 0] = [];
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_071():
    source = """
func main() -> void {
    let a: [int; 1] = [];
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", ArrayType(IntType(), 1), ArrayLiteral([])))
    assert Checker(source).check_from_source() == str(expected)


def test_072():
    source = """
func main() -> void {
    let a:string = "S" + 1;
    let b:string = "S" + true;
    let c:string = "S" + 1.0;
    let d:string = "S" + "s";
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_073():
    source = """
func foo() -> int {
}
func main() -> void {
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_074():
    source = """
func main() -> void {
    1;
    return;
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_075():
    source = """
func foo() -> void {
    print("");
    return;
} 
    
func main() -> void {
    let a = 5;
    a >> foo;
    return;
}
"""
    expected =  'Type Mismatch In Statement: ExprStmt(BinaryOp(Identifier(a), >>, Identifier(foo)))'
    assert Checker(source).check_from_source() == str(expected)


def test_076():
    source = """
func foo(a: int) -> void {
    print(int2str(a));
    return;
} 
    
func main() -> void {
    let a = 5;
    a >> foo;
    return;
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_077():
    source = """
func main() -> void {
    print(float2str(1.0));
}
"""
    expected =  "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)


def test_078():
    source = """
func main() -> void {
    let a: int = len([1, 2, 3]);
    print("" + a);
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_079():
    source = """
func foo() -> void {
    let arr = [1.0, 1, 2, 3];
    print(int2str(arr[0]));
}
func main() -> void {
    foo();
}
"""
    expected =  'Type Mismatch In Expression: ArrayLiteral([FloatLiteral(1.0), IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])'
    assert Checker(source).check_from_source() == str(expected)


def test_080():
    source = """
func main() -> void {
    foo();
}
"""
    expected =  "Undeclared Function: foo"
    assert Checker(source).check_from_source() == str(expected)


def test_081():
    source = """
const A: [int; 1] = [10];
func main() -> void {
    print(A);
}
"""
    expected =  "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(print), [Identifier(A)]))"
    assert Checker(source).check_from_source() == str(expected)


def test_082():
    source = """
func main() -> void {
    !5;
}
"""
    expected =  "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(5))"
    assert Checker(source).check_from_source() == str(expected)


def test_083():
    source = """
func main() -> void {
    let input = input();
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_084():
    source = """
func print() -> void {
}
func main() -> void {
    return;
}
"""
    expected =  'Redeclared Function: print'
    assert Checker(source).check_from_source() == str(expected)


def test_085():
    source = """
func len() -> void {
}
func main() -> void {
    return;
}
"""
    expected =  'Redeclared Function: len'
    assert Checker(source).check_from_source() == str(expected)


def test_086():
    source = """
func str2int() -> void {
}
func main() -> void {
    return;
}
"""
    expected =  'Redeclared Function: str2int'
    assert Checker(source).check_from_source() == str(expected)


def test_087():
    source = """
func float2str() -> void {
}
func main() -> void {
    return;
}
"""
    expected =  'Redeclared Function: float2str'
    assert Checker(source).check_from_source() == str(expected)


def test_088():
    source = """
func str2int() -> void {
}
func main() -> void {
    return;
}
"""
    expected =  'Redeclared Function: str2int'
    assert Checker(source).check_from_source() == str(expected)


def test_089():
    source = """
func main() -> void {
    float2str(1.5);
}
"""
    expected =  "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(float2str), [FloatLiteral(1.5)]))"
    assert Checker(source).check_from_source() == str(expected)


def test_090():
    source = """
func main() -> void {
    let a: string = float2str(1.5);
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_091():
    source = """
func main() -> void {
    let main = 5;
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_092():
    source = """
func main() -> void {
    let arr: [int; 1] = [1];
    let a = arr >> len;
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_093():
    source = """
func main() -> void {
    int2str(10) >> print;
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_094():
    source = """
func main() -> void {
    float2str(10) >> print;
}
"""
    expected =  "Type Mismatch In Statement: ExprStmt(BinaryOp(FunctionCall(Identifier(float2str), [IntegerLiteral(10)]), >>, Identifier(print)))"
    assert Checker(source).check_from_source() == str(expected)


def test_095():
    source = """
func main() -> void {
    str2int("10") >> print;
}
"""
    expected =  "Type Mismatch In Statement: ExprStmt(BinaryOp(FunctionCall(Identifier(str2int), [StringLiteral('10')]), >>, Identifier(print)))"
    assert Checker(source).check_from_source() == str(expected)


def test_096():
    source = """
func main() -> void {
    str2float("10.0") >> print;
}
"""
    expected =  "Type Mismatch In Statement: ExprStmt(BinaryOp(FunctionCall(Identifier(str2float), [StringLiteral('10.0')]), >>, Identifier(print)))"
    assert Checker(source).check_from_source() == str(expected)


def test_097():
    source = """
func main() -> void {
    print("Principle");
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_098():
    source = """
func main() -> void {
    print("Programming");
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_099():
    source = """
func main() -> void {
    print("Language");
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


def test_100():
    source = """
func main() -> void {
    print("Thanks PPL :v");
}
"""
    expected =  'Static checking passed'
    assert Checker(source).check_from_source() == str(expected)


