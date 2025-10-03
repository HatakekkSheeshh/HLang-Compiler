from utils import ASTGenerator

def test_000():
    """Test basic constant declaration AST generation"""
    source = """const x: int = 42;
    """
    expected = '''Program(consts=[ConstDecl(x, int, IntegerLiteral(42))])'''
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


def test_001():
    """Test function declaration AST generation"""
    source = "func main() -> void {}"
    expected = "Program(funcs=[FuncDecl(main, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    """Test function with parameters AST generation"""
    source = "func add(a: int, b: int) -> int { return a + b; }"
    expected = "Program(funcs=[FuncDecl(add, [Param(a, int), Param(b, int)], int, [ReturnStmt(BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    """Test multiple declarations AST generation"""
    source = """const PI: float = 3.14;
    func square(x: int) -> int { return x * x; }"""
    expected = "Program(consts=[ConstDecl(PI, float, FloatLiteral(3.14))], funcs=[FuncDecl(square, [Param(x, int)], int, [ReturnStmt(BinaryOp(Identifier(x), *, Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice"; }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(name, StringLiteral('Alice'))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    """Test if-else statement AST generation"""
    source = """func main() -> void { 
        if (x > 0) { 
            return x;
        } else { 
            return 0;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([ReturnStmt(Identifier(x))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007a():
    """Test while loop AST generation"""
    source = """func main() -> void { 
        while (i < 10) { 
            i = i + 1; 
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007b():
    """Test array operations AST generation"""
    source = """func main() -> void { 
        let arr = [1, 2, 3];
        let first = arr[0];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])), VarDecl(first, ArrayAccess(Identifier(arr), IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009a():
    """Test less_than operator AST generation"""
    source = """func main() -> void { 
        let result = a < b;
    }"""
    expected = '''Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(Identifier(a), <, Identifier(b)))])])'''
    assert str(ASTGenerator(source).generate()) == expected


def test_009b():
    """Test pipeline operator AST generation"""
    source = """func main() -> void { 
        let result = data >> process;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(Identifier(data), >>, Identifier(process)))])])"
    assert str(ASTGenerator(source).generate()) == expected



def test_010():
    source = '''
        const a = [];
        const a = [1];
        const a = [true, 2.5, "hi"];
        const a = [[], [1, 2], 2];
    '''
    expected = "Program(consts=[ConstDecl(a, ArrayLiteral([])), ConstDecl(a, ArrayLiteral([IntegerLiteral(1)])), ConstDecl(a, ArrayLiteral([BooleanLiteral(True), FloatLiteral(2.5), StringLiteral('hi')])), ConstDecl(a, ArrayLiteral([ArrayLiteral([]), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), IntegerLiteral(2)]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_011():
    source = """
        const a = a + b;
        const a = (1 + 2) * 3;
    """
    expected = "Program(consts=[ConstDecl(a, BinaryOp(Identifier(a), +, Identifier(b))), ConstDecl(a, BinaryOp(BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)), *, IntegerLiteral(3)))])"   
    assert str(ASTGenerator(source).generate()) == expected
        

def test_012():
    source = """
        const a = foo();
        const a = foo(1);
        const b = foo(1, [], foo());
    """
    expected = "Program(consts=[ConstDecl(a, FunctionCall(Identifier(foo), [])), ConstDecl(a, FunctionCall(Identifier(foo), [IntegerLiteral(1)])), ConstDecl(b, FunctionCall(Identifier(foo), [IntegerLiteral(1), ArrayLiteral([]), FunctionCall(Identifier(foo), [])]))])"
    assert str(ASTGenerator(source).generate()) == expected  


def test_013():
    source = """
        const a = int(1);
        const a = float();
        const a = int() + float(1,2);
    """
    expected = "Program(consts=[ConstDecl(a, FunctionCall(Identifier(int), [IntegerLiteral(1)])), ConstDecl(a, FunctionCall(Identifier(float), [])), ConstDecl(a, BinaryOp(FunctionCall(Identifier(int), []), +, FunctionCall(Identifier(float), [IntegerLiteral(1), IntegerLiteral(2)])))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_014():
    source = """
        func foo() -> void {
            foo(1) + int();
            a[2] >> b;
            foo()[1][2];
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [ExprStmt(BinaryOp(FunctionCall(Identifier(foo), [IntegerLiteral(1)]), +, FunctionCall(Identifier(int), []))), ExprStmt(BinaryOp(ArrayAccess(Identifier(a), IntegerLiteral(2)), >>, Identifier(b))), ExprStmt(ArrayAccess(ArrayAccess(FunctionCall(Identifier(foo), []), IntegerLiteral(1)), IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_015():
    source = """
        func foo() -> void {
            a = 1;
            a[2] = foo() >> a[2];
            a[a[2]][1+2] = 1;
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [Assignment(IdLValue(a), IntegerLiteral(1)), Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(2)), BinaryOp(FunctionCall(Identifier(foo), []), >>, ArrayAccess(Identifier(a), IntegerLiteral(2)))), Assignment(ArrayAccessLValue(ArrayAccess(Identifier(a), ArrayAccess(Identifier(a), IntegerLiteral(2))), BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2))), IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_016():
    source = '''
        const a = 42;
        const b = 3.14;
        const c = "hello";
        const d = true;
        const e = false;
    '''
    expected = "Program(consts=[ConstDecl(a, IntegerLiteral(42)), ConstDecl(b, FloatLiteral(3.14)), ConstDecl(c, StringLiteral('hello')), ConstDecl(d, BooleanLiteral(True)), ConstDecl(e, BooleanLiteral(False))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_017():
    source = '''
    func total() -> int {
        let a = [1,2,3,4,5,6,7,8,9,10] ;
        let length = len(a) ;
        let total = 0 ;
        for (i in (length - 1)) {
            total = total + len ;
        }
        
        return total ;
    }
    '''
    expected = "Program(funcs=[FuncDecl(total, [], int, [VarDecl(a, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6), IntegerLiteral(7), IntegerLiteral(8), IntegerLiteral(9), IntegerLiteral(10)])), VarDecl(length, FunctionCall(Identifier(len), [Identifier(a)])), VarDecl(total, IntegerLiteral(0)), ForStmt(i, BinaryOp(Identifier(length), -, IntegerLiteral(1)), BlockStmt([Assignment(IdLValue(total), BinaryOp(Identifier(total), +, Identifier(len)))])), ReturnStmt(Identifier(total))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_018():
    source = """
        const a = 42;
        const b = 3.14;
        const c = "hello";
        const d = true;
        const e = a;
    """
    expected = "Program(consts=[ConstDecl(a, IntegerLiteral(42)), ConstDecl(b, FloatLiteral(3.14)), ConstDecl(c, StringLiteral('hello')), ConstDecl(d, BooleanLiteral(True)), ConstDecl(e, Identifier(a))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_019():
    source = """
        const a = [];
        const a = [1];
        const a = [true, 2.5, \"hi\"];
        const a = [[], [1, 2], 2];
    """
    expected = "Program(consts=[ConstDecl(a, ArrayLiteral([])), ConstDecl(a, ArrayLiteral([IntegerLiteral(1)])), ConstDecl(a, ArrayLiteral([BooleanLiteral(True), FloatLiteral(2.5), StringLiteral('hi')])), ConstDecl(a, ArrayLiteral([ArrayLiteral([]), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), IntegerLiteral(2)]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_020():
    source = """
        func foo() -> void {}
        func foo() -> string {}
        func foo() -> [int; 2] {}
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, []), FuncDecl(foo, [], string, []), FuncDecl(foo, [], [int; 2], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_021():
    source = """
        func foo() -> void {
            foo(1) + int();
            a[2] >> b;
            foo()[1][2];
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [ExprStmt(BinaryOp(FunctionCall(Identifier(foo), [IntegerLiteral(1)]), +, FunctionCall(Identifier(int), []))), ExprStmt(BinaryOp(ArrayAccess(Identifier(a), IntegerLiteral(2)), >>, Identifier(b))), ExprStmt(ArrayAccess(ArrayAccess(FunctionCall(Identifier(foo), []), IntegerLiteral(1)), IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected
    

def test_023():
    source = '''
    func total() -> int {
        let a = [1,2,3,4,5,6,7,8,9,10] ;
        let length = len(a) ;
        let total = 0 ;
        for (i in (length - 1)) {
            total = total + len ;
        }
        
        return total ;
    }
    '''
    expected = "Program(funcs=[FuncDecl(total, [], int, [VarDecl(a, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6), IntegerLiteral(7), IntegerLiteral(8), IntegerLiteral(9), IntegerLiteral(10)])), VarDecl(length, FunctionCall(Identifier(len), [Identifier(a)])), VarDecl(total, IntegerLiteral(0)), ForStmt(i, BinaryOp(Identifier(length), -, IntegerLiteral(1)), BlockStmt([Assignment(IdLValue(total), BinaryOp(Identifier(total), +, Identifier(len)))])), ReturnStmt(Identifier(total))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_024():
    """Expression"""
    source = ''' 
    func calc() -> float {
        let x = (1 + 2) * 3 / 4 % 2;
        let y = -x + !true && false || true;
        let z = x <= y && y >= x || x != y;
        return x >> y >> z;
    }
    '''
    expected = "Program(funcs=[FuncDecl(calc, [], float, [VarDecl(x, BinaryOp(BinaryOp(BinaryOp(BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)), *, IntegerLiteral(3)), /, IntegerLiteral(4)), %, IntegerLiteral(2))), VarDecl(y, BinaryOp(BinaryOp(BinaryOp(UnaryOp(-, Identifier(x)), +, UnaryOp(!, BooleanLiteral(True))), &&, BooleanLiteral(False)), ||, BooleanLiteral(True))), VarDecl(z, BinaryOp(BinaryOp(BinaryOp(Identifier(x), <=, Identifier(y)), &&, BinaryOp(Identifier(y), >=, Identifier(x))), ||, BinaryOp(Identifier(x), !=, Identifier(y)))), ReturnStmt(BinaryOp(BinaryOp(Identifier(x), >>, Identifier(y)), >>, Identifier(z)))])])"
    print(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_025():
    """Condition Statement"""
    source = ''' 
    func max(a: int, b: int) -> int {
        if (a > b) {
            return a;
        } else if (a < b) {
            return b;
        } else {
            return a; // equal case
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(max, [Param(a, int), Param(b, int)], int, [IfStmt(condition=BinaryOp(Identifier(a), >, Identifier(b)), then_stmt=BlockStmt([ReturnStmt(Identifier(a))]), elif_branches=[(BinaryOp(Identifier(a), <, Identifier(b)), BlockStmt([ReturnStmt(Identifier(b))]))], else_stmt=BlockStmt([ReturnStmt(Identifier(a))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_026():
    """Loop statement"""
    source = ''' 
    func main() -> void {
        let i = 0;
        while (i < 10) {
            i = i + 1;
            if (i == 5) {
                continue;
            }
            if (i == 8) {
                break;
            }
        }

        for (x in 10) {
            print(x);
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(i, IntegerLiteral(0)), WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1))), IfStmt(condition=BinaryOp(Identifier(i), ==, IntegerLiteral(5)), then_stmt=BlockStmt([ContinueStmt()])), IfStmt(condition=BinaryOp(Identifier(i), ==, IntegerLiteral(8)), then_stmt=BlockStmt([BreakStmt()]))])), ForStmt(x, IntegerLiteral(10), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [Identifier(x)]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_027():
    source = ''' 
    func main() -> void {
        let arr: [int; 3] = [1, 2, 3];
        let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, [int; 3], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])), VarDecl(matrix, [[int; 2]; 2], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_028():
    source = ''' 
    func main() -> void {
        let x: int = 5;
        let y: float = 3.14;
        let s: string = "hello";
        let b: bool = true;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, int, IntegerLiteral(5)), VarDecl(y, float, FloatLiteral(3.14)), VarDecl(s, string, StringLiteral('hello')), VarDecl(b, bool, BooleanLiteral(True))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_029():
    """Function calls and Nested expressions"""
    source = '''
    func complex_calc(x: int, y: float) -> float {
        let a = float(x) + len(str(y));
        let b = int(float(x) * y / 2.0);
        let result = max(float(a), float(b)) + min(a, int(b));
        return result;
    } 
    '''
    expected = "Program(funcs=[FuncDecl(complex_calc, [Param(x, int), Param(y, float)], float, [VarDecl(a, BinaryOp(FunctionCall(Identifier(float), [Identifier(x)]), +, FunctionCall(Identifier(len), [FunctionCall(Identifier(str), [Identifier(y)])]))), VarDecl(b, FunctionCall(Identifier(int), [BinaryOp(BinaryOp(FunctionCall(Identifier(float), [Identifier(x)]), *, Identifier(y)), /, FloatLiteral(2.0))])), VarDecl(result, BinaryOp(FunctionCall(Identifier(max), [FunctionCall(Identifier(float), [Identifier(a)]), FunctionCall(Identifier(float), [Identifier(b)])]), +, FunctionCall(Identifier(min), [Identifier(a), FunctionCall(Identifier(int), [Identifier(b)])]))), ReturnStmt(Identifier(result))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_030():
    source = ''' 
    '''
    expected = '''Program()'''
    assert str(ASTGenerator(source).generate()) == expected


def test_031():
    """Test unary expressions with different operators"""
    source = '''
    func main() -> void {
        let a = -5;
        let b = +3.14;
        let c = !true;
        let d = -(x + y);
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(a, UnaryOp(-, IntegerLiteral(5))), VarDecl(b, UnaryOp(+, FloatLiteral(3.14))), VarDecl(c, UnaryOp(!, BooleanLiteral(True))), VarDecl(d, UnaryOp(-, BinaryOp(Identifier(x), +, Identifier(y))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_032():
    """Test nested array access expressions"""
    source = '''
    func main() -> void {
        let matrix = [[1, 2], [3, 4]];
        let value = matrix[0][1];
        let deep = arr[i][j][k];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(matrix, ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])])), VarDecl(value, ArrayAccess(ArrayAccess(Identifier(matrix), IntegerLiteral(0)), IntegerLiteral(1))), VarDecl(deep, ArrayAccess(ArrayAccess(ArrayAccess(Identifier(arr), Identifier(i)), Identifier(j)), Identifier(k)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_033():
    """Test complex pipeline expressions"""
    source = '''
    func main() -> void {
        let result = data >> filter(isValid) >> map(transform) >> reduce(sum);
        let chained = x >> f1 >> f2(arg) >> f3;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(BinaryOp(BinaryOp(Identifier(data), >>, FunctionCall(Identifier(filter), [Identifier(isValid)])), >>, FunctionCall(Identifier(map), [Identifier(transform)])), >>, FunctionCall(Identifier(reduce), [Identifier(sum)]))), VarDecl(chained, BinaryOp(BinaryOp(BinaryOp(Identifier(x), >>, Identifier(f1)), >>, FunctionCall(Identifier(f2), [Identifier(arg)])), >>, Identifier(f3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_034():
    """Test array type declarations with different sizes"""
    source = '''
    const small: [int; 1] = [42];
    const medium: [float; 5] = [1.0, 2.0, 3.0, 4.0, 5.0];
    const large: [string; 10] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"];
    '''
    expected = "Program(consts=[ConstDecl(small, [int; 1], ArrayLiteral([IntegerLiteral(42)])), ConstDecl(medium, [float; 5], ArrayLiteral([FloatLiteral(1.0), FloatLiteral(2.0), FloatLiteral(3.0), FloatLiteral(4.0), FloatLiteral(5.0)])), ConstDecl(large, [string; 10], ArrayLiteral([StringLiteral('a'), StringLiteral('b'), StringLiteral('c'), StringLiteral('d'), StringLiteral('e'), StringLiteral('f'), StringLiteral('g'), StringLiteral('h'), StringLiteral('i'), StringLiteral('j')]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_035():
    """Test multi-dimensional array types"""
    source = '''
    func main() -> void {
        let matrix2d: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
        let cube3d: [[[bool; 2]; 2]; 2] = [[[true, false], [false, true]], [[true, true], [false, false]]];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(matrix2d, [[int; 3]; 2], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), ArrayLiteral([IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6)])])), VarDecl(cube3d, [[[bool; 2]; 2]; 2], ArrayLiteral([ArrayLiteral([ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False)]), ArrayLiteral([BooleanLiteral(False), BooleanLiteral(True)])]), ArrayLiteral([ArrayLiteral([BooleanLiteral(True), BooleanLiteral(True)]), ArrayLiteral([BooleanLiteral(False), BooleanLiteral(False)])])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_036():
    """Test complex lvalue assignments"""
    source = '''
    func main() -> void {
        matrix[i + 1][j * 2] = value;
        arr[calculate(x)][y] = compute(z);
        data[indices[0]][indices[1]] = result;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccessLValue(ArrayAccess(Identifier(matrix), BinaryOp(Identifier(i), +, IntegerLiteral(1))), BinaryOp(Identifier(j), *, IntegerLiteral(2))), Identifier(value)), Assignment(ArrayAccessLValue(ArrayAccess(Identifier(arr), FunctionCall(Identifier(calculate), [Identifier(x)])), Identifier(y)), FunctionCall(Identifier(compute), [Identifier(z)])), Assignment(ArrayAccessLValue(ArrayAccess(Identifier(data), ArrayAccess(Identifier(indices), IntegerLiteral(0))), ArrayAccess(Identifier(indices), IntegerLiteral(1))), Identifier(result))])])"
    print(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_037():
    """Test all primitive type literals"""
    source = '''
    const intVal = 42;
    const negInt = -17;
    const floatVal = 3.14159;
    const expFloat = 1.23e-4;
    const stringVal = "Hello, World!";
    const boolTrue = true;
    const boolFalse = false;
    '''
    expected = "Program(consts=[ConstDecl(intVal, IntegerLiteral(42)), ConstDecl(negInt, UnaryOp(-, IntegerLiteral(17))), ConstDecl(floatVal, FloatLiteral(3.14159)), ConstDecl(expFloat, FloatLiteral(0.000123)), ConstDecl(stringVal, StringLiteral('Hello, World!')), ConstDecl(boolTrue, BooleanLiteral(True)), ConstDecl(boolFalse, BooleanLiteral(False))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_038():
    """Test function parameters with different types"""
    source = '''
    func process(id: int, name: string, score: float, active: bool, data: [int; 5]) -> void {
        print("Processing");
    }
    '''
    expected = "Program(funcs=[FuncDecl(process, [Param(id, int), Param(name, string), Param(score, float), Param(active, bool), Param(data, [int; 5])], void, [ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Processing')]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_039():
    """Test function return types"""
    source = '''
    func getInt() -> int { return 42; }
    func getFloat() -> float { return 3.14; }
    func getString() -> string { return "hello"; }
    func getBool() -> bool { return true; }
    func getArray() -> [int; 3] { return [1, 2, 3]; }
    func doNothing() -> void { print("done"); }
    '''
    expected = "Program(funcs=[FuncDecl(getInt, [], int, [ReturnStmt(IntegerLiteral(42))]), FuncDecl(getFloat, [], float, [ReturnStmt(FloatLiteral(3.14))]), FuncDecl(getString, [], string, [ReturnStmt(StringLiteral('hello'))]), FuncDecl(getBool, [], bool, [ReturnStmt(BooleanLiteral(True))]), FuncDecl(getArray, [], [int; 3], [ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))]), FuncDecl(doNothing, [], void, [ExprStmt(FunctionCall(Identifier(print), [StringLiteral('done')]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_040():
    """Test mixed arithmetic and comparison expressions"""
    source = '''
    func main() -> void {
        let result1 = (a + b) * c / d % e;
        let result2 = x < y && z > w || p == q;
        let result3 = (i <= j) && (k >= l) && (m != n);
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result1, BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, Identifier(c)), /, Identifier(d)), %, Identifier(e))), VarDecl(result2, BinaryOp(BinaryOp(BinaryOp(Identifier(x), <, Identifier(y)), &&, BinaryOp(Identifier(z), >, Identifier(w))), ||, BinaryOp(Identifier(p), ==, Identifier(q)))), VarDecl(result3, BinaryOp(BinaryOp(BinaryOp(Identifier(i), <=, Identifier(j)), &&, BinaryOp(Identifier(k), >=, Identifier(l))), &&, BinaryOp(Identifier(m), !=, Identifier(n))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_041():
    """Test nested if-elif-else statements"""
    source = '''
    func classify(score: int) -> string {
        if (score >= 90) {
            return "A";
        } else if (score >= 80) {
            return "B";
        } else if (score >= 70) {
            return "C";
        } else if (score >= 60) {
            return "D";
        } else {
            return "F";
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(classify, [Param(score, int)], string, [IfStmt(condition=BinaryOp(Identifier(score), >=, IntegerLiteral(90)), then_stmt=BlockStmt([ReturnStmt(StringLiteral('A'))]), elif_branches=[(BinaryOp(Identifier(score), >=, IntegerLiteral(80)), BlockStmt([ReturnStmt(StringLiteral('B'))])), (BinaryOp(Identifier(score), >=, IntegerLiteral(70)), BlockStmt([ReturnStmt(StringLiteral('C'))])), (BinaryOp(Identifier(score), >=, IntegerLiteral(60)), BlockStmt([ReturnStmt(StringLiteral('D'))]))], else_stmt=BlockStmt([ReturnStmt(StringLiteral('F'))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_042():
    """Test for loops with different iterables"""
    source = '''
    func main() -> void {
        for (item in items) {
            print(str(item));
        }
        for (number in numbers) {
            if (number > 0) {
                continue;
            }
            break;
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(item, Identifier(items), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(item)])]))])), ForStmt(number, Identifier(numbers), BlockStmt([IfStmt(condition=BinaryOp(Identifier(number), >, IntegerLiteral(0)), then_stmt=BlockStmt([ContinueStmt()])), BreakStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_043():
    """Test while loops with complex conditions"""
    source = '''
    func main() -> void {
        while (i < n && !found) {
            i = i + 1;
            if (arr[i] == target) {
                found = true;
            }
        }
        while ((x > 0) || (y < 10)) {
            x = x - 1;
            y = y + 1;
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(BinaryOp(Identifier(i), <, Identifier(n)), &&, UnaryOp(!, Identifier(found))), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1))), IfStmt(condition=BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), ==, Identifier(target)), then_stmt=BlockStmt([Assignment(IdLValue(found), BooleanLiteral(True))]))])), WhileStmt(BinaryOp(BinaryOp(Identifier(x), >, IntegerLiteral(0)), ||, BinaryOp(Identifier(y), <, IntegerLiteral(10))), BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), -, IntegerLiteral(1))), Assignment(IdLValue(y), BinaryOp(Identifier(y), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_044():
    """Test built-in function calls"""
    source = '''
    func main() -> void {
        let numStr = str(42);
        let floatStr = str(3.14);
        let boolStr = str(true);
        let num = int("123");
        let decimal = float("3.14");
        let length = len(array);
        print("Hello");
        let input_data = input();
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(numStr, FunctionCall(Identifier(str), [IntegerLiteral(42)])), VarDecl(floatStr, FunctionCall(Identifier(str), [FloatLiteral(3.14)])), VarDecl(boolStr, FunctionCall(Identifier(str), [BooleanLiteral(True)])), VarDecl(num, FunctionCall(Identifier(int), [StringLiteral('123')])), VarDecl(decimal, FunctionCall(Identifier(float), [StringLiteral('3.14')])), VarDecl(length, FunctionCall(Identifier(len), [Identifier(array)])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Hello')])), VarDecl(input_data, FunctionCall(Identifier(input), []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_045():
    """Test parenthesized expressions for precedence"""
    source = '''
    func main() -> void {
        let a = (x + y) * (z - w);
        let b = !(flag1 && flag2) || flag3;
        let c = (arr[i] + arr[j]) / (count + 1);
        let d = ((a > b) && (c < d)) || ((e == f) && (g != h));
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(a, BinaryOp(BinaryOp(Identifier(x), +, Identifier(y)), *, BinaryOp(Identifier(z), -, Identifier(w)))), VarDecl(b, BinaryOp(UnaryOp(!, BinaryOp(Identifier(flag1), &&, Identifier(flag2))), ||, Identifier(flag3))), VarDecl(c, BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), +, ArrayAccess(Identifier(arr), Identifier(j))), /, BinaryOp(Identifier(count), +, IntegerLiteral(1)))), VarDecl(d, BinaryOp(BinaryOp(BinaryOp(Identifier(a), >, Identifier(b)), &&, BinaryOp(Identifier(c), <, Identifier(d))), ||, BinaryOp(BinaryOp(Identifier(e), ==, Identifier(f)), &&, BinaryOp(Identifier(g), !=, Identifier(h)))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_046():
    """Test expression statements"""
    source = '''
    func main() -> void {
        x + y;
        func_call();
        arr[0];
        process(data);
        getValue();
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(BinaryOp(Identifier(x), +, Identifier(y))), ExprStmt(FunctionCall(Identifier(func_call), [])), ExprStmt(ArrayAccess(Identifier(arr), IntegerLiteral(0))), ExprStmt(FunctionCall(Identifier(process), [Identifier(data)])), ExprStmt(FunctionCall(Identifier(getValue), []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_047():
    """Test block statements and scoping"""
    source = '''
    func main() -> void {
        let x = 10;
        {
            let y = 20;
            {
                let z = 30;
                print(str(x + y + z));
            }
            print(str(x + y));
        }
        print(str(x));
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, IntegerLiteral(10)), BlockStmt([VarDecl(y, IntegerLiteral(20)), BlockStmt([VarDecl(z, IntegerLiteral(30)), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [BinaryOp(BinaryOp(Identifier(x), +, Identifier(y)), +, Identifier(z))])]))]), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [BinaryOp(Identifier(x), +, Identifier(y))])]))]), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(x)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_048():
    """Test break and continue statements in nested loops"""
    source = '''
    func main() -> void {
        for (i in outer) {
            for (j in inner) {
                if (condition1) {
                    break;
                }
                if (condition2) {
                    continue;
                }
                process(i, j);
            }
            print("Outer loop");
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(i, Identifier(outer), BlockStmt([ForStmt(j, Identifier(inner), BlockStmt([IfStmt(condition=Identifier(condition1), then_stmt=BlockStmt([BreakStmt()])), IfStmt(condition=Identifier(condition2), then_stmt=BlockStmt([ContinueStmt()])), ExprStmt(FunctionCall(Identifier(process), [Identifier(i), Identifier(j)]))])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Outer loop')]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_049():
    """Test return statements with different expressions"""
    source = '''
    func getValue() -> int { return 42; }
    func getSum(a: int, b: int) -> int { return a + b; }
    func getArray() -> [int; 3] { return [1, 2, 3]; }
    func doWork() -> void { return; }
    func getComplex() -> float { return calculate(x) + arr[i]; }
    '''
    expected = "Program(funcs=[FuncDecl(getValue, [], int, [ReturnStmt(IntegerLiteral(42))]), FuncDecl(getSum, [Param(a, int), Param(b, int)], int, [ReturnStmt(BinaryOp(Identifier(a), +, Identifier(b)))]), FuncDecl(getArray, [], [int; 3], [ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))]), FuncDecl(doWork, [], void, [ReturnStmt()]), FuncDecl(getComplex, [], float, [ReturnStmt(BinaryOp(FunctionCall(Identifier(calculate), [Identifier(x)]), +, ArrayAccess(Identifier(arr), Identifier(i))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_050():
    """Test complex nested function calls"""
    source = '''
    func main() -> void {
        let result = func1(func2(x, y), func3(arr[0], func4()));
        let chained = process(filter(data, predicate), transform);
        let nested = outer(inner(deep(value, param)));
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, FunctionCall(Identifier(func1), [FunctionCall(Identifier(func2), [Identifier(x), Identifier(y)]), FunctionCall(Identifier(func3), [ArrayAccess(Identifier(arr), IntegerLiteral(0)), FunctionCall(Identifier(func4), [])])])), VarDecl(chained, FunctionCall(Identifier(process), [FunctionCall(Identifier(filter), [Identifier(data), Identifier(predicate)]), Identifier(transform)])), VarDecl(nested, FunctionCall(Identifier(outer), [FunctionCall(Identifier(inner), [FunctionCall(Identifier(deep), [Identifier(value), Identifier(param)])])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_051():
    """Test all comparison operators"""
    source = '''
    func main() -> void {
        let eq = a == b;
        let neq = a != b;
        let lt = a < b;
        let leq = a <= b;
        let gt = a > b;
        let geq = a >= b;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(eq, BinaryOp(Identifier(a), ==, Identifier(b))), VarDecl(neq, BinaryOp(Identifier(a), !=, Identifier(b))), VarDecl(lt, BinaryOp(Identifier(a), <, Identifier(b))), VarDecl(leq, BinaryOp(Identifier(a), <=, Identifier(b))), VarDecl(gt, BinaryOp(Identifier(a), >, Identifier(b))), VarDecl(geq, BinaryOp(Identifier(a), >=, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_052():
    """Test all logical operators"""
    source = '''
    func main() -> void {
        let and_result = flag1 && flag2;
        let or_result = flag1 || flag2;
        let not_result = !flag1;
        let complex = (a && b) || (!c && d);
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(and_result, BinaryOp(Identifier(flag1), &&, Identifier(flag2))), VarDecl(or_result, BinaryOp(Identifier(flag1), ||, Identifier(flag2))), VarDecl(not_result, UnaryOp(!, Identifier(flag1))), VarDecl(complex, BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, BinaryOp(UnaryOp(!, Identifier(c)), &&, Identifier(d))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_053():
    """Test all arithmetic operators"""
    source = '''
    func main() -> void {
        let add = a + b;
        let sub = a - b;
        let mul = a * b;
        let div = a / b;
        let mod = a % b;
        let complex = (a + b) * (c - d) / (e % f);
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(add, BinaryOp(Identifier(a), +, Identifier(b))), VarDecl(sub, BinaryOp(Identifier(a), -, Identifier(b))), VarDecl(mul, BinaryOp(Identifier(a), *, Identifier(b))), VarDecl(div, BinaryOp(Identifier(a), /, Identifier(b))), VarDecl(mod, BinaryOp(Identifier(a), %, Identifier(b))), VarDecl(complex, BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, BinaryOp(Identifier(c), -, Identifier(d))), /, BinaryOp(Identifier(e), %, Identifier(f))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_054():
    """Test string literals with escape sequences"""
    source = '''
    const message1 = "Hello\\nWorld";
    const message2 = "Quote: \\"text\\"";
    const message3 = "Tab\\tSeparated";
    const message4 = "Backslash: \\\\";
    const message5 = "Return\\rCarriage";
    '''
    expected = "Program(consts=[ConstDecl(message1, StringLiteral('Hello\\\\nWorld')), ConstDecl(message2, StringLiteral('Quote: \\\\\"text\\\\\"')), ConstDecl(message3, StringLiteral('Tab\\\\tSeparated')), ConstDecl(message4, StringLiteral('Backslash: \\\\\\\\')), ConstDecl(message5, StringLiteral('Return\\\\rCarriage'))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_055():
    """Test mixed type array literals"""
    source = '''
    func main() -> void {
        let intArray = [1, 2, 3, 4, 5];
        let floatArray = [1.0, 2.5, 3.14, 4.7];
        let stringArray = ["hello", "world", "test"];
        let boolArray = [true, false, true, false];
        let emptyArray = [];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(intArray, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])), VarDecl(floatArray, ArrayLiteral([FloatLiteral(1.0), FloatLiteral(2.5), FloatLiteral(3.14), FloatLiteral(4.7)])), VarDecl(stringArray, ArrayLiteral([StringLiteral('hello'), StringLiteral('world'), StringLiteral('test')])), VarDecl(boolArray, ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True), BooleanLiteral(False)])), VarDecl(emptyArray, ArrayLiteral([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_056():
    """Test operator precedence with mixed operations"""
    source = '''
    func main() -> void {
        let result1 = a + b * c;
        let result2 = a * b + c;
        let result3 = a && b || c;
        let result4 = a || b && c;
        let result5 = !a && b;
        let result6 = a >> b + c;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result1, BinaryOp(Identifier(a), +, BinaryOp(Identifier(b), *, Identifier(c)))), VarDecl(result2, BinaryOp(BinaryOp(Identifier(a), *, Identifier(b)), +, Identifier(c))), VarDecl(result3, BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, Identifier(c))), VarDecl(result4, BinaryOp(Identifier(a), ||, BinaryOp(Identifier(b), &&, Identifier(c)))), VarDecl(result5, BinaryOp(UnaryOp(!, Identifier(a)), &&, Identifier(b))), VarDecl(result6, BinaryOp(Identifier(a), >>, BinaryOp(Identifier(b), +, Identifier(c))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_057():
    """Test function calls with array arguments"""
    source = '''
    func main() -> void {
        process([1, 2, 3]);
        handle(arr, [4, 5, 6]);
        let result = compute([x, y, z], [[1, 2], [3, 4]]);
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(process), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])])), ExprStmt(FunctionCall(Identifier(handle), [Identifier(arr), ArrayLiteral([IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6)])])), VarDecl(result, FunctionCall(Identifier(compute), [ArrayLiteral([Identifier(x), Identifier(y), Identifier(z)]), ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_058():
    """Test constants with complex expressions"""
    source = '''
    const COMPUTED = x + y * z;
    const ARRAY_SIZE = len(data);
    const MESSAGE = "Value: " + str(value);
    const CONDITION = (x > 0) && (y < 10);
    const PIPELINE_RESULT = data >> filter >> first;
    '''
    expected = "Program(consts=[ConstDecl(COMPUTED, BinaryOp(Identifier(x), +, BinaryOp(Identifier(y), *, Identifier(z)))), ConstDecl(ARRAY_SIZE, FunctionCall(Identifier(len), [Identifier(data)])), ConstDecl(MESSAGE, BinaryOp(StringLiteral('Value: '), +, FunctionCall(Identifier(str), [Identifier(value)]))), ConstDecl(CONDITION, BinaryOp(BinaryOp(Identifier(x), >, IntegerLiteral(0)), &&, BinaryOp(Identifier(y), <, IntegerLiteral(10)))), ConstDecl(PIPELINE_RESULT, BinaryOp(BinaryOp(Identifier(data), >>, Identifier(filter)), >>, Identifier(first)))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_059():
    """Test variable declarations with type annotations"""
    source = '''
    func main() -> void {
        let x: int = 42;
        let y: float = 3.14;
        let s: string = "hello";
        let flag: bool = true;
        let arr: [int; 5] = [1, 2, 3, 4, 5];
        let matrix: [[float; 2]; 3] = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, int, IntegerLiteral(42)), VarDecl(y, float, FloatLiteral(3.14)), VarDecl(s, string, StringLiteral('hello')), VarDecl(flag, bool, BooleanLiteral(True)), VarDecl(arr, [int; 5], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])), VarDecl(matrix, [[float; 2]; 3], ArrayLiteral([ArrayLiteral([FloatLiteral(1.0), FloatLiteral(2.0)]), ArrayLiteral([FloatLiteral(3.0), FloatLiteral(4.0)]), ArrayLiteral([FloatLiteral(5.0), FloatLiteral(6.0)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_060():
    """Test constant declarations with type annotations"""
    source = '''
    const MAX_SIZE: int = 100;
    const PI_VALUE: float = 3.14159;
    const APP_NAME: string = "HLang Compiler";
    const DEBUG_MODE: bool = false;
    const PRIMES: [int; 5] = [2, 3, 5, 7, 11];
    '''
    expected = "Program(consts=[ConstDecl(MAX_SIZE, int, IntegerLiteral(100)), ConstDecl(PI_VALUE, float, FloatLiteral(3.14159)), ConstDecl(APP_NAME, string, StringLiteral('HLang Compiler')), ConstDecl(DEBUG_MODE, bool, BooleanLiteral(False)), ConstDecl(PRIMES, [int; 5], ArrayLiteral([IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(5), IntegerLiteral(7), IntegerLiteral(11)]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_061():
    """Test pipeline with function calls and operators"""
    source = '''
    func main() -> void {
        let result1 = data >> filter(isValid) >> map(transform) >> reduce;
        let result2 = value >> func1 >> func2(arg1, arg2) >> func3;
        let result3 = array >> process >> [0] >> getValue;
        let result4 = x + y >> compute >> result * 2;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result1, BinaryOp(BinaryOp(BinaryOp(Identifier(data), >>, FunctionCall(Identifier(filter), [Identifier(isValid)])), >>, FunctionCall(Identifier(map), [Identifier(transform)])), >>, Identifier(reduce))), VarDecl(result2, BinaryOp(BinaryOp(BinaryOp(Identifier(value), >>, Identifier(func1)), >>, FunctionCall(Identifier(func2), [Identifier(arg1), Identifier(arg2)])), >>, Identifier(func3))), VarDecl(result3, BinaryOp(BinaryOp(BinaryOp(Identifier(array), >>, Identifier(process)), >>, ArrayLiteral([IntegerLiteral(0)])), >>, Identifier(getValue))), VarDecl(result4, BinaryOp(BinaryOp(BinaryOp(Identifier(x), +, Identifier(y)), >>, Identifier(compute)), >>, BinaryOp(Identifier(result), *, IntegerLiteral(2))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_062():
    """Test nested blocks with variable declarations"""
    source = '''
    func main() -> void {
        let outer = 1;
        {
            let inner1 = 2;
            {
                let inner2 = 3;
                {
                    let inner3 = 4;
                    let sum = outer + inner1 + inner2 + inner3;
                }
            }
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(outer, IntegerLiteral(1)), BlockStmt([VarDecl(inner1, IntegerLiteral(2)), BlockStmt([VarDecl(inner2, IntegerLiteral(3)), BlockStmt([VarDecl(inner3, IntegerLiteral(4)), VarDecl(sum, BinaryOp(BinaryOp(BinaryOp(Identifier(outer), +, Identifier(inner1)), +, Identifier(inner2)), +, Identifier(inner3)))])])])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_063():
    """Test complex if statements with nested conditions"""
    source = '''
    func main() -> void {
        if ((a > b) && (c < d)) {
            if (flag) {
                process();
            } else {
                handle();
            }
        } else if ((x == y) || (z != w)) {
            alternative();
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(BinaryOp(Identifier(a), >, Identifier(b)), &&, BinaryOp(Identifier(c), <, Identifier(d))), then_stmt=BlockStmt([IfStmt(condition=Identifier(flag), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(process), []))]), else_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(handle), []))]))]), elif_branches=[(BinaryOp(BinaryOp(Identifier(x), ==, Identifier(y)), ||, BinaryOp(Identifier(z), !=, Identifier(w))), BlockStmt([ExprStmt(FunctionCall(Identifier(alternative), []))]))])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_064():
    """Test array access with complex indices"""
    source = '''
    func main() -> void {
        let val1 = arr[i + j];
        let val2 = matrix[calculate(x)][compute(y, z)];
        let val3 = data[indices[0]][indices[1] + offset];
        let val4 = nested[outer[i]][inner[j]][deep[k]];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(val1, ArrayAccess(Identifier(arr), BinaryOp(Identifier(i), +, Identifier(j)))), VarDecl(val2, ArrayAccess(ArrayAccess(Identifier(matrix), FunctionCall(Identifier(calculate), [Identifier(x)])), FunctionCall(Identifier(compute), [Identifier(y), Identifier(z)]))), VarDecl(val3, ArrayAccess(ArrayAccess(Identifier(data), ArrayAccess(Identifier(indices), IntegerLiteral(0))), BinaryOp(ArrayAccess(Identifier(indices), IntegerLiteral(1)), +, Identifier(offset)))), VarDecl(val4, ArrayAccess(ArrayAccess(ArrayAccess(Identifier(nested), ArrayAccess(Identifier(outer), Identifier(i))), ArrayAccess(Identifier(inner), Identifier(j))), ArrayAccess(Identifier(deep), Identifier(k))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_065():
    """Test function calls with no arguments"""
    source = '''
    func main() -> void {
        getValue();
        let x = compute();
        let y = process() + getValue();
        print(getMessage());
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(getValue), [])), VarDecl(x, FunctionCall(Identifier(compute), [])), VarDecl(y, BinaryOp(FunctionCall(Identifier(process), []), +, FunctionCall(Identifier(getValue), []))), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(getMessage), [])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_066():
    """Test function calls with single argument"""
    source = '''
    func main() -> void {
        process(x);
        let y = compute(42);
        print(str(value));
        handle([1, 2, 3]);
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(process), [Identifier(x)])), VarDecl(y, FunctionCall(Identifier(compute), [IntegerLiteral(42)])), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(value)])])), ExprStmt(FunctionCall(Identifier(handle), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_067():
    """Test function calls with multiple arguments"""
    source = '''
    func main() -> void {
        add(x, y);
        let result = compute(a, b, c);
        process(data, config, handler);
        print(format(name, age, score));
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(add), [Identifier(x), Identifier(y)])), VarDecl(result, FunctionCall(Identifier(compute), [Identifier(a), Identifier(b), Identifier(c)])), ExprStmt(FunctionCall(Identifier(process), [Identifier(data), Identifier(config), Identifier(handler)])), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(format), [Identifier(name), Identifier(age), Identifier(score)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_068():
    """Test assignment to array elements"""
    source = '''
    func main() -> void {
        arr[0] = 42;
        matrix[i][j] = value;
        data[calculate(x)][y + z] = compute();
        nested[a][b][c] = result;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(42)), Assignment(ArrayAccessLValue(ArrayAccess(Identifier(matrix), Identifier(i)), Identifier(j)), Identifier(value)), Assignment(ArrayAccessLValue(ArrayAccess(Identifier(data), FunctionCall(Identifier(calculate), [Identifier(x)])), BinaryOp(Identifier(y), +, Identifier(z))), FunctionCall(Identifier(compute), [])), Assignment(ArrayAccessLValue(ArrayAccess(ArrayAccess(Identifier(nested), Identifier(a)), Identifier(b)), Identifier(c)), Identifier(result))])])"
    print(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_069():
    """Test assignment with complex expressions"""
    source = '''
    func main() -> void {
        x = y + z * w;
        arr[i] = calculate(a, b) + c;
        result = getValue(data);
        total = sum >> filter(positive) >> reduce;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(IdLValue(x), BinaryOp(Identifier(y), +, BinaryOp(Identifier(z), *, Identifier(w)))), Assignment(ArrayAccessLValue(Identifier(arr), Identifier(i)), BinaryOp(FunctionCall(Identifier(calculate), [Identifier(a), Identifier(b)]), +, Identifier(c))), Assignment(IdLValue(result), FunctionCall(Identifier(getValue), [Identifier(data)])), Assignment(IdLValue(total), BinaryOp(BinaryOp(Identifier(sum), >>, FunctionCall(Identifier(filter), [Identifier(positive)])), >>, Identifier(reduce)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_070():
    """Test large array literals"""
    source = '''
    const LARGE_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
    const FLOAT_ARRAY = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9];
    const STRING_ARRAY = ["a", "b", "c", "d", "e", "f", "g", "h"];
    '''
    expected = "Program(consts=[ConstDecl(LARGE_ARRAY, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6), IntegerLiteral(7), IntegerLiteral(8), IntegerLiteral(9), IntegerLiteral(10), IntegerLiteral(11), IntegerLiteral(12), IntegerLiteral(13), IntegerLiteral(14), IntegerLiteral(15), IntegerLiteral(16), IntegerLiteral(17), IntegerLiteral(18), IntegerLiteral(19), IntegerLiteral(20)])), ConstDecl(FLOAT_ARRAY, ArrayLiteral([FloatLiteral(1.1), FloatLiteral(2.2), FloatLiteral(3.3), FloatLiteral(4.4), FloatLiteral(5.5), FloatLiteral(6.6), FloatLiteral(7.7), FloatLiteral(8.8), FloatLiteral(9.9)])), ConstDecl(STRING_ARRAY, ArrayLiteral([StringLiteral('a'), StringLiteral('b'), StringLiteral('c'), StringLiteral('d'), StringLiteral('e'), StringLiteral('f'), StringLiteral('g'), StringLiteral('h')]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_071():
    """Test deeply nested array literals"""
    source = '''
    const DEEP_NESTED = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]];
    const MIXED_DEEP = [[[true, false], [false, true]], [[false, false], [true, true]]];
    '''
    expected = "Program(consts=[ConstDecl(DEEP_NESTED, ArrayLiteral([ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])]), ArrayLiteral([ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6)]), ArrayLiteral([IntegerLiteral(7), IntegerLiteral(8)])])])), ConstDecl(MIXED_DEEP, ArrayLiteral([ArrayLiteral([ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False)]), ArrayLiteral([BooleanLiteral(False), BooleanLiteral(True)])]), ArrayLiteral([ArrayLiteral([BooleanLiteral(False), BooleanLiteral(False)]), ArrayLiteral([BooleanLiteral(True), BooleanLiteral(True)])])]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_072():
    """Test functions with many parameters"""
    source = '''
    func manyParams(a: int, b: float, c: string, d: bool, e: [int; 3], f: [[float; 2]; 2]) -> void {
        print("Many parameters");
    }
    '''
    expected = "Program(funcs=[FuncDecl(manyParams, [Param(a, int), Param(b, float), Param(c, string), Param(d, bool), Param(e, [int; 3]), Param(f, [[float; 2]; 2])], void, [ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Many parameters')]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_073():
    """Test complex function body with multiple statements"""
    source = '''
    func complexFunction(data: [int; 10], threshold: int) -> int {
        let count = 0;
        let total = 0;
        for (item in data) {
            if (item > threshold) {
                count = count + 1;
                total = total + item;
            }
        }
        if (count > 0) {
            return total / count;
        } else {
            return 0;
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(complexFunction, [Param(data, [int; 10]), Param(threshold, int)], int, [VarDecl(count, IntegerLiteral(0)), VarDecl(total, IntegerLiteral(0)), ForStmt(item, Identifier(data), BlockStmt([IfStmt(condition=BinaryOp(Identifier(item), >, Identifier(threshold)), then_stmt=BlockStmt([Assignment(IdLValue(count), BinaryOp(Identifier(count), +, IntegerLiteral(1))), Assignment(IdLValue(total), BinaryOp(Identifier(total), +, Identifier(item)))]))])), IfStmt(condition=BinaryOp(Identifier(count), >, IntegerLiteral(0)), then_stmt=BlockStmt([ReturnStmt(BinaryOp(Identifier(total), /, Identifier(count)))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_074():
    """Test edge case with zero-sized arrays"""
    source = '''
    const EMPTY: [int; 0] = [];
    func main() -> void {
        let emptyFloat: [float; 0] = [];
        let emptyString: [string; 0] = [];
    }
    '''
    expected = "Program(consts=[ConstDecl(EMPTY, [int; 0], ArrayLiteral([]))], funcs=[FuncDecl(main, [], void, [VarDecl(emptyFloat, [float; 0], ArrayLiteral([])), VarDecl(emptyString, [string; 0], ArrayLiteral([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_075():
    """Test scientific notation float literals"""
    source = '''
    const AVOGADRO = 6.022e23;
    const PLANCK = 6.626e-34;
    const LIGHT_SPEED = 2.998E8;
    const ELECTRON_MASS = 9.109E-31;
    func main() -> void {
        let small = 1.5e-10;
        let large = 3.7E15;
    }
    '''
    expected = "Program(consts=[ConstDecl(AVOGADRO, FloatLiteral(6.022e+23)), ConstDecl(PLANCK, FloatLiteral(6.626e-34)), ConstDecl(LIGHT_SPEED, FloatLiteral(299800000.0)), ConstDecl(ELECTRON_MASS, FloatLiteral(9.109e-31))], funcs=[FuncDecl(main, [], void, [VarDecl(small, FloatLiteral(1.5e-10)), VarDecl(large, FloatLiteral(3700000000000000.0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_076():
    """Test mixed constants and functions"""
    source = '''
    const VERSION = "1.0.0";
    const MAX_USERS = 1000;
    func getVersion() -> string { return VERSION; }
    func getMaxUsers() -> int { return MAX_USERS; }
    '''
    expected = "Program(consts=[ConstDecl(VERSION, StringLiteral('1.0.0')), ConstDecl(MAX_USERS, IntegerLiteral(1000))], funcs=[FuncDecl(getVersion, [], string, [ReturnStmt(Identifier(VERSION))]), FuncDecl(getMaxUsers, [], int, [ReturnStmt(Identifier(MAX_USERS))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_077():
    """Test recursive function definition"""
    source = '''
    func factorial(n: int) -> int {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(factorial, [Param(n, int)], int, [IfStmt(condition=BinaryOp(Identifier(n), <=, IntegerLiteral(1)), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))]), else_stmt=BlockStmt([ReturnStmt(BinaryOp(Identifier(n), *, FunctionCall(Identifier(factorial), [BinaryOp(Identifier(n), -, IntegerLiteral(1))])))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_078():
    """Test function with array manipulation"""
    source = '''
    func sumArray(arr: [int; 5]) -> int {
        let total = 0;
        for (i in arr) {
            total = total + i;
        }
        return total;
    }
    '''
    expected = "Program(funcs=[FuncDecl(sumArray, [Param(arr, [int; 5])], int, [VarDecl(total, IntegerLiteral(0)), ForStmt(i, Identifier(arr), BlockStmt([Assignment(IdLValue(total), BinaryOp(Identifier(total), +, Identifier(i)))])), ReturnStmt(Identifier(total))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_079():
    """Test early return patterns"""
    source = '''
    func findElement(arr: [int; 10], target: int) -> int {
        for (i in arr) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    '''
    expected = "Program(funcs=[FuncDecl(findElement, [Param(arr, [int; 10]), Param(target, int)], int, [ForStmt(i, Identifier(arr), BlockStmt([IfStmt(condition=BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), ==, Identifier(target)), then_stmt=BlockStmt([ReturnStmt(Identifier(i))]))])), ReturnStmt(UnaryOp(-, IntegerLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_080():
    """Test complex boolean expressions"""
    source = '''
    func isValidRange(x: int, min: int, max: int) -> bool {
        return (x >= min) && (x <= max) && (min < max);
    }
    '''
    expected = "Program(funcs=[FuncDecl(isValidRange, [Param(x, int), Param(min, int), Param(max, int)], bool, [ReturnStmt(BinaryOp(BinaryOp(BinaryOp(Identifier(x), >=, Identifier(min)), &&, BinaryOp(Identifier(x), <=, Identifier(max))), &&, BinaryOp(Identifier(min), <, Identifier(max))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_081():
    """Test string operations and concatenation"""
    source = '''
    func formatMessage(name: string, age: int) -> string {
        return "Name: " + name + ", Age: " + str(age);
    }
    '''
    expected = "Program(funcs=[FuncDecl(formatMessage, [Param(name, string), Param(age, int)], string, [ReturnStmt(BinaryOp(BinaryOp(BinaryOp(StringLiteral('Name: '), +, Identifier(name)), +, StringLiteral(', Age: ')), +, FunctionCall(Identifier(str), [Identifier(age)])))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_082():
    """Test matrix operations"""
    source = '''
    func getMatrixElement(matrix: [[int; 3]; 3], row: int, col: int) -> int {
        return matrix[row][col];
    }
    '''
    expected = "Program(funcs=[FuncDecl(getMatrixElement, [Param(matrix, [[int; 3]; 3]), Param(row, int), Param(col, int)], int, [ReturnStmt(ArrayAccess(ArrayAccess(Identifier(matrix), Identifier(row)), Identifier(col)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_083():
    """Test nested function calls with complex arguments"""
    source = '''
    func main() -> void {
        let result = func1(func2(a + b), func3(arr[i], func4(c * d)));
        process(compute(x, y), transform(data[0], data[1]));
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, FunctionCall(Identifier(func1), [FunctionCall(Identifier(func2), [BinaryOp(Identifier(a), +, Identifier(b))]), FunctionCall(Identifier(func3), [ArrayAccess(Identifier(arr), Identifier(i)), FunctionCall(Identifier(func4), [BinaryOp(Identifier(c), *, Identifier(d))])])])), ExprStmt(FunctionCall(Identifier(process), [FunctionCall(Identifier(compute), [Identifier(x), Identifier(y)]), FunctionCall(Identifier(transform), [ArrayAccess(Identifier(data), IntegerLiteral(0)), ArrayAccess(Identifier(data), IntegerLiteral(1))])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_084():
    """Test while loop with multiple conditions and complex body"""
    source = '''
    func processData(data: [int; 100]) -> void {
        let i = 0;
        while ((i < len(data)) && (data[i] > 0)) {
            if (data[i] % 2 == 0) {
                data[i] = data[i] / 2;
            } else {
                data[i] = data[i] * 3 + 1;
            }
            i = i + 1;
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(processData, [Param(data, [int; 100])], void, [VarDecl(i, IntegerLiteral(0)), WhileStmt(BinaryOp(BinaryOp(Identifier(i), <, FunctionCall(Identifier(len), [Identifier(data)])), &&, BinaryOp(ArrayAccess(Identifier(data), Identifier(i)), >, IntegerLiteral(0))), BlockStmt([IfStmt(condition=BinaryOp(BinaryOp(ArrayAccess(Identifier(data), Identifier(i)), %, IntegerLiteral(2)), ==, IntegerLiteral(0)), then_stmt=BlockStmt([Assignment(ArrayAccessLValue(Identifier(data), Identifier(i)), BinaryOp(ArrayAccess(Identifier(data), Identifier(i)), /, IntegerLiteral(2)))]), else_stmt=BlockStmt([Assignment(ArrayAccessLValue(Identifier(data), Identifier(i)), BinaryOp(BinaryOp(ArrayAccess(Identifier(data), Identifier(i)), *, IntegerLiteral(3)), +, IntegerLiteral(1)))])), Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_085():
    """Test variable shadowing in nested blocks"""
    source = '''
    func shadowingExample() -> void {
        let x = 1;
        {
            let x = 2;
            {
                let x = 3;
                print(str(x));
            }
            print(str(x));
        }
        print(str(x));
    }
    '''
    expected = "Program(funcs=[FuncDecl(shadowingExample, [], void, [VarDecl(x, IntegerLiteral(1)), BlockStmt([VarDecl(x, IntegerLiteral(2)), BlockStmt([VarDecl(x, IntegerLiteral(3)), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(x)])]))]), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(x)])]))]), ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(x)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_086():
    """Test complex pipeline operations"""
    source = '''
    func main() -> void {
        let result = data >> filter(isPositive) >> map(square) >> reduce(sum) >> str;
        let processed = input >> parse >> validate >> transform >> output;
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(data), >>, FunctionCall(Identifier(filter), [Identifier(isPositive)])), >>, FunctionCall(Identifier(map), [Identifier(square)])), >>, FunctionCall(Identifier(reduce), [Identifier(sum)])), >>, Identifier(str))), VarDecl(processed, BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(input), >>, Identifier(parse)), >>, Identifier(validate)), >>, Identifier(transform)), >>, Identifier(output)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_087():
    """Test all unary operators with different expressions"""
    source = '''
    func main() -> void {
        let neg = -value;
        let pos = +value;
        let not_val = !condition;
        let complex = -(a + b);
        let nested = !(!flag);
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(neg, UnaryOp(-, Identifier(value))), VarDecl(pos, UnaryOp(+, Identifier(value))), VarDecl(not_val, UnaryOp(!, Identifier(condition))), VarDecl(complex, UnaryOp(-, BinaryOp(Identifier(a), +, Identifier(b)))), VarDecl(nested, UnaryOp(!, UnaryOp(!, Identifier(flag))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_088():
    """Test function calls as array indices"""
    source = '''
    func main() -> void {
        let val1 = arr[getIndex()];
        let val2 = matrix[func1(x)][func2(y)];
        let val3 = data[compute(a, b)];
        matrix[getRow()][getCol()] = getValue();
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(val1, ArrayAccess(Identifier(arr), FunctionCall(Identifier(getIndex), []))), VarDecl(val2, ArrayAccess(ArrayAccess(Identifier(matrix), FunctionCall(Identifier(func1), [Identifier(x)])), FunctionCall(Identifier(func2), [Identifier(y)]))), VarDecl(val3, ArrayAccess(Identifier(data), FunctionCall(Identifier(compute), [Identifier(a), Identifier(b)]))), Assignment(ArrayAccessLValue(ArrayAccess(Identifier(matrix), FunctionCall(Identifier(getRow), [])), FunctionCall(Identifier(getCol), [])), FunctionCall(Identifier(getValue), []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_089():
    """Test mixed literal types in arrays"""
    source = '''
    func main() -> void {
        let intArray = [0, 42, -17, 1000, -999];
        let floatArray = [0.0, 3.14, -2.5, 1.5e10, -1.23e-4];
        let boolArray = [true, false, true, true, false];
        let stringArray = ["", "hello", "world", "test", "end"];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(intArray, ArrayLiteral([IntegerLiteral(0), IntegerLiteral(42), UnaryOp(-, IntegerLiteral(17)), IntegerLiteral(1000), UnaryOp(-, IntegerLiteral(999))])), VarDecl(floatArray, ArrayLiteral([FloatLiteral(0.0), FloatLiteral(3.14), UnaryOp(-, FloatLiteral(2.5)), FloatLiteral(15000000000.0), UnaryOp(-, FloatLiteral(0.000123))])), VarDecl(boolArray, ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True), BooleanLiteral(True), BooleanLiteral(False)])), VarDecl(stringArray, ArrayLiteral([StringLiteral(''), StringLiteral('hello'), StringLiteral('world'), StringLiteral('test'), StringLiteral('end')]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_090():
    """Test function with void return and multiple statements"""
    source = '''
    func printReport(title: string, data: [int; 5]) -> void {
        print(title);
        print("Data:");
        for (item in data) {
            print(str(item));
        }
        print("End of report");
    }
    '''
    expected = "Program(funcs=[FuncDecl(printReport, [Param(title, string), Param(data, [int; 5])], void, [ExprStmt(FunctionCall(Identifier(print), [Identifier(title)])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Data:')])), ForStmt(item, Identifier(data), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(item)])]))])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('End of report')]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_091():
    """Test nested loops with break and continue"""
    source = '''
    func findPair(matrix: [[int; 10]; 10], target: int) -> void {
        for (row in matrix) {
            for (col in row) {
                if (row[col] == target) {
                    print("Found");
                    break;
                }
                if (row[col] < 0) {
                    continue;
                }
                process(row[col]);
            }
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(findPair, [Param(matrix, [[int; 10]; 10]), Param(target, int)], void, [ForStmt(row, Identifier(matrix), BlockStmt([ForStmt(col, Identifier(row), BlockStmt([IfStmt(condition=BinaryOp(ArrayAccess(Identifier(row), Identifier(col)), ==, Identifier(target)), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Found')])), BreakStmt()])), IfStmt(condition=BinaryOp(ArrayAccess(Identifier(row), Identifier(col)), <, IntegerLiteral(0)), then_stmt=BlockStmt([ContinueStmt()])), ExprStmt(FunctionCall(Identifier(process), [ArrayAccess(Identifier(row), Identifier(col))]))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_092():
    """Test complex conditional assignments"""
    source = '''
    func main() -> void {
        if (a > b) {
            max = a;
        } else {
            max = b;
        }
        if (flag) {
            arr[i] = value1;
        } else {
            arr[i] = value2;
        }
        if (x > 0) {
            result = y + 1;
        } else {
            result = y - 1;
        }
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(a), >, Identifier(b)), then_stmt=BlockStmt([Assignment(IdLValue(max), Identifier(a))]), else_stmt=BlockStmt([Assignment(IdLValue(max), Identifier(b))])), IfStmt(condition=Identifier(flag), then_stmt=BlockStmt([Assignment(ArrayAccessLValue(Identifier(arr), Identifier(i)), Identifier(value1))]), else_stmt=BlockStmt([Assignment(ArrayAccessLValue(Identifier(arr), Identifier(i)), Identifier(value2))])), IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([Assignment(IdLValue(result), BinaryOp(Identifier(y), +, IntegerLiteral(1)))]), else_stmt=BlockStmt([Assignment(IdLValue(result), BinaryOp(Identifier(y), -, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_093():
    """Test array initialization with expressions"""
    source = '''
    func main() -> void {
        let computed = [a + b, c * d, e / f, g % h];
        let mixed = [calculate(x), arr[i], value, 42];
        let nested = [[a, b], [c, d], [e, f]];
    }
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(computed, ArrayLiteral([BinaryOp(Identifier(a), +, Identifier(b)), BinaryOp(Identifier(c), *, Identifier(d)), BinaryOp(Identifier(e), /, Identifier(f)), BinaryOp(Identifier(g), %, Identifier(h))])), VarDecl(mixed, ArrayLiteral([FunctionCall(Identifier(calculate), [Identifier(x)]), ArrayAccess(Identifier(arr), Identifier(i)), Identifier(value), IntegerLiteral(42)])), VarDecl(nested, ArrayLiteral([ArrayLiteral([Identifier(a), Identifier(b)]), ArrayLiteral([Identifier(c), Identifier(d)]), ArrayLiteral([Identifier(e), Identifier(f)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_094():
    """Test complex return expressions"""
    source = '''
    func computeResult(a: int, b: int, c: int) -> int {
        return (a + b) * c / (a - b) + (c % a);
    }
    func getBestValue(arr: [int; 5]) -> int {
        return arr[findMaxIndex(arr)];
    }
    '''
    expected = "Program(funcs=[FuncDecl(computeResult, [Param(a, int), Param(b, int), Param(c, int)], int, [ReturnStmt(BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, Identifier(c)), /, BinaryOp(Identifier(a), -, Identifier(b))), +, BinaryOp(Identifier(c), %, Identifier(a))))]), FuncDecl(getBestValue, [Param(arr, [int; 5])], int, [ReturnStmt(ArrayAccess(Identifier(arr), FunctionCall(Identifier(findMaxIndex), [Identifier(arr)])))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_095():
    """Test input/output operations"""
    source = '''
    func interactive() -> void {
        print("Enter your name:");
        let name = input();
        print("Hello, " + name + "!");
        print("Enter a number:");
        let numStr = input();
        let num = int(numStr);
        print("Your number squared is: " + str(num * num));
    }
    '''
    expected = "Program(funcs=[FuncDecl(interactive, [], void, [ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Enter your name:')])), VarDecl(name, FunctionCall(Identifier(input), [])), ExprStmt(FunctionCall(Identifier(print), [BinaryOp(BinaryOp(StringLiteral('Hello, '), +, Identifier(name)), +, StringLiteral('!'))])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Enter a number:')])), VarDecl(numStr, FunctionCall(Identifier(input), [])), VarDecl(num, FunctionCall(Identifier(int), [Identifier(numStr)])), ExprStmt(FunctionCall(Identifier(print), [BinaryOp(StringLiteral('Your number squared is: '), +, FunctionCall(Identifier(str), [BinaryOp(Identifier(num), *, Identifier(num))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_096():
    """Test error handling patterns"""
    source = '''
    func safeDivide(a: int, b: int) -> int {
        if (b == 0) {
            print("Error: Division by zero");
            return -1;
        }
        return a / b;
    }
    '''
    expected = "Program(funcs=[FuncDecl(safeDivide, [Param(a, int), Param(b, int)], int, [IfStmt(condition=BinaryOp(Identifier(b), ==, IntegerLiteral(0)), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Error: Division by zero')])), ReturnStmt(UnaryOp(-, IntegerLiteral(1)))])), ReturnStmt(BinaryOp(Identifier(a), /, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_097():
    """Test utility functions with multiple features"""
    source = '''
    func reverseArray(arr: [int; 5]) -> [int; 5] {
        let reversed: [int; 5] = [0, 0, 0, 0, 0];
        let length = len(arr);
        for (i in arr) {
            reversed[length - 1 - i] = arr[i];
        }
        return reversed;
    }
    '''
    expected = "Program(funcs=[FuncDecl(reverseArray, [Param(arr, [int; 5])], [int; 5], [VarDecl(reversed, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), VarDecl(length, FunctionCall(Identifier(len), [Identifier(arr)])), ForStmt(i, Identifier(arr), BlockStmt([Assignment(ArrayAccessLValue(Identifier(reversed), BinaryOp(BinaryOp(Identifier(length), -, IntegerLiteral(1)), -, Identifier(i))), ArrayAccess(Identifier(arr), Identifier(i)))])), ReturnStmt(Identifier(reversed))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_098():
    """Test comprehensive program with all features"""
    source = '''
    const MAX_SIZE = 100;
    const PI = 3.14159;
    
    func calculate(data: [float; 10], factor: float) -> float {
        let sum = 0.0;
        for (value in data) {
            if (value > 0.0) {
                sum = sum + (value * factor);
            }
        }
        return sum / len(data);
    }
    
    func main() -> void {
        let numbers: [float; 10] = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
        let result = calculate(numbers, PI);
        print("Average: " + str(result));
    }
    '''
    expected = "Program(consts=[ConstDecl(MAX_SIZE, IntegerLiteral(100)), ConstDecl(PI, FloatLiteral(3.14159))], funcs=[FuncDecl(calculate, [Param(data, [float; 10]), Param(factor, float)], float, [VarDecl(sum, FloatLiteral(0.0)), ForStmt(value, Identifier(data), BlockStmt([IfStmt(condition=BinaryOp(Identifier(value), >, FloatLiteral(0.0)), then_stmt=BlockStmt([Assignment(IdLValue(sum), BinaryOp(Identifier(sum), +, BinaryOp(Identifier(value), *, Identifier(factor))))]))])), ReturnStmt(BinaryOp(Identifier(sum), /, FunctionCall(Identifier(len), [Identifier(data)])))]), FuncDecl(main, [], void, [VarDecl(numbers, [float; 10], ArrayLiteral([FloatLiteral(1.0), FloatLiteral(2.0), FloatLiteral(3.0), FloatLiteral(4.0), FloatLiteral(5.0), FloatLiteral(6.0), FloatLiteral(7.0), FloatLiteral(8.0), FloatLiteral(9.0), FloatLiteral(10.0)])), VarDecl(result, FunctionCall(Identifier(calculate), [Identifier(numbers), Identifier(PI)])), ExprStmt(FunctionCall(Identifier(print), [BinaryOp(StringLiteral('Average: '), +, FunctionCall(Identifier(str), [Identifier(result)]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_099():
    """Test edge case with minimal valid program"""
    source = '''
    func main() -> void {}
    '''
    expected = "Program(funcs=[FuncDecl(main, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_100():
    """Test comprehensive edge cases and special scenarios"""
    source = '''
    const EMPTY_ARRAY: [int; 0] = [];
    const SINGLE_ITEM: [string; 1] = ["only"];
    
    func edgeCases() -> void {
        let x = 0;
        let y = 0.0;
        let z = "";
        let w = false;
        
        while (false) {
            break;
        }
        
        for (item in EMPTY_ARRAY) {
            continue;
        }
        
        if (true) {
            return;
        }
        
        x = 0;
        y = 0;
        z = 0;
        w = 0;
    }
    '''
    expected = "Program(consts=[ConstDecl(EMPTY_ARRAY, [int; 0], ArrayLiteral([])), ConstDecl(SINGLE_ITEM, [string; 1], ArrayLiteral([StringLiteral('only')]))], funcs=[FuncDecl(edgeCases, [], void, [VarDecl(x, IntegerLiteral(0)), VarDecl(y, FloatLiteral(0.0)), VarDecl(z, StringLiteral('')), VarDecl(w, BooleanLiteral(False)), WhileStmt(BooleanLiteral(False), BlockStmt([BreakStmt()])), ForStmt(item, Identifier(EMPTY_ARRAY), BlockStmt([ContinueStmt()])), IfStmt(condition=BooleanLiteral(True), then_stmt=BlockStmt([ReturnStmt()])), Assignment(IdLValue(x), IntegerLiteral(0)), Assignment(IdLValue(y), IntegerLiteral(0)), Assignment(IdLValue(z), IntegerLiteral(0)), Assignment(IdLValue(w), IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_101():
    """Test edge case with minimal valid program"""
    source = '''
    func foo() -> void {}
    func main() -> void {
        foo();
        goo();
    }
    '''
    expected = "Program(funcs=[FuncDecl(foo, [], void, []), FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(foo), [])), ExprStmt(FunctionCall(Identifier(goo), []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_102():
    source = """
    func main() -> void {
        a[1][2] = 1;
    }
    """
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccessLValue(ArrayAccess(Identifier(a), IntegerLiteral(1)), IntegerLiteral(2)), IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_103():
    source = """
    func main() -> void {
        break ;
        continue ;
        a + b >> c ;
        k = !a + !b ;
    }
    """
    expected = "Program(funcs=[FuncDecl(main, [], void, [BreakStmt(), ContinueStmt(), ExprStmt(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), >>, Identifier(c))), Assignment(IdLValue(k), BinaryOp(UnaryOp(!, Identifier(a)), +, UnaryOp(!, Identifier(b))))])])"
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_104():
    """All instructions for stmt"""
    source = """
    func all(a: int, b: int) -> int {
        let var: int = 1 + 2 + 3 + 4 + 5 ;
        ass = all() + a + b ;
        if(a > b){
            return a ;
        }
        else if(a < b){
            return b ;
        }
        else{
            return (a || b) ;
        }
            
        while(a < 5) {
            a = a + 1 ;
            break ;
        }
        for(b in arr) {
            b = b + 2 ;
            continue ;
        }
        {
            let var: int = 1 + 2 + 3 + 4 + 5 ;
            ass = all() + a + b ;
            if(a > b){
                return a ;
            }
            else if(a < b){
                return b ;
            }
            else{
                return (a || b) ;
            }
                
            while(a < 5) {
                a = a + 1 ;
                break ;
            }
            for(b in arr) {
                b = b + 2 ;
                continue ;
            }
        }
    }
    """
    expected = "Program(funcs=[FuncDecl(all, [Param(a, int), Param(b, int)], int, [VarDecl(var, int, BinaryOp(BinaryOp(BinaryOp(BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)), +, IntegerLiteral(3)), +, IntegerLiteral(4)), +, IntegerLiteral(5))), Assignment(IdLValue(ass), BinaryOp(BinaryOp(FunctionCall(Identifier(all), []), +, Identifier(a)), +, Identifier(b))), IfStmt(condition=BinaryOp(Identifier(a), >, Identifier(b)), then_stmt=BlockStmt([ReturnStmt(Identifier(a))]), elif_branches=[(BinaryOp(Identifier(a), <, Identifier(b)), BlockStmt([ReturnStmt(Identifier(b))]))], else_stmt=BlockStmt([ReturnStmt(BinaryOp(Identifier(a), ||, Identifier(b)))])), WhileStmt(BinaryOp(Identifier(a), <, IntegerLiteral(5)), BlockStmt([Assignment(IdLValue(a), BinaryOp(Identifier(a), +, IntegerLiteral(1))), BreakStmt()])), ForStmt(b, Identifier(arr), BlockStmt([Assignment(IdLValue(b), BinaryOp(Identifier(b), +, IntegerLiteral(2))), ContinueStmt()])), BlockStmt([VarDecl(var, int, BinaryOp(BinaryOp(BinaryOp(BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)), +, IntegerLiteral(3)), +, IntegerLiteral(4)), +, IntegerLiteral(5))), Assignment(IdLValue(ass), BinaryOp(BinaryOp(FunctionCall(Identifier(all), []), +, Identifier(a)), +, Identifier(b))), IfStmt(condition=BinaryOp(Identifier(a), >, Identifier(b)), then_stmt=BlockStmt([ReturnStmt(Identifier(a))]), elif_branches=[(BinaryOp(Identifier(a), <, Identifier(b)), BlockStmt([ReturnStmt(Identifier(b))]))], else_stmt=BlockStmt([ReturnStmt(BinaryOp(Identifier(a), ||, Identifier(b)))])), WhileStmt(BinaryOp(Identifier(a), <, IntegerLiteral(5)), BlockStmt([Assignment(IdLValue(a), BinaryOp(Identifier(a), +, IntegerLiteral(1))), BreakStmt()])), ForStmt(b, Identifier(arr), BlockStmt([Assignment(IdLValue(b), BinaryOp(Identifier(b), +, IntegerLiteral(2))), ContinueStmt()]))])])])"
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_105():
    """Test all expression"""
    source = """
    func expr() -> void {
        a >> expr() || b && c == d != e < f <= g >= h > i + j - k * l / m % n + -1 - +5 >> arr[5][4][3] >> (kkk + kkk) >> a + [4, 3, 2, 1] ; 
    }
    """
    expected = "Program(funcs=[FuncDecl(expr, [], void, [ExprStmt(BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(a), >>, BinaryOp(FunctionCall(Identifier(expr), []), ||, BinaryOp(Identifier(b), &&, BinaryOp(BinaryOp(Identifier(c), ==, Identifier(d)), !=, BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(e), <, Identifier(f)), <=, Identifier(g)), >=, Identifier(h)), >, BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(i), +, Identifier(j)), -, BinaryOp(BinaryOp(BinaryOp(Identifier(k), *, Identifier(l)), /, Identifier(m)), %, Identifier(n))), +, UnaryOp(-, IntegerLiteral(1))), -, UnaryOp(+, IntegerLiteral(5)))))))), >>, ArrayAccess(ArrayAccess(ArrayAccess(Identifier(arr), IntegerLiteral(5)), IntegerLiteral(4)), IntegerLiteral(3))), >>, BinaryOp(Identifier(kkk), +, Identifier(kkk))), >>, BinaryOp(Identifier(a), +, ArrayLiteral([IntegerLiteral(4), IntegerLiteral(3), IntegerLiteral(2), IntegerLiteral(1)]))))])])"
    assert str(ASTGenerator(source).generate()) == str(expected)