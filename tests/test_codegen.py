from src.utils.nodes import *

from utils import CodeGenerator

def test_001():
    source = """
func main() -> void {
    print("Hello World");
}
"""
    expected = "Hello World"
    assert CodeGenerator().generate_and_run(source) == expected

def test_002():
    source = """
func main() -> void {
    print(int2str(1));
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_003():
    source = """
func main() -> void {
    let i: float = 1.0 - 2;
    print(float2str(i));
}
"""
    expected = "-1.0"
    assert CodeGenerator().generate_and_run(source) == expected
    
def test_004():
    source = """
func main() -> void {
    let i: int = 3 / 2;
    print(int2str(i));
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected
    
################### String ###################
def test_005():
    source = """
func main() -> void {
    print(bool2str("s1" != "s1"));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_006():
    source = """
func main() -> void {
    print(bool2str("s2" == "s2"));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_007():
    source = """
func main() -> void {
    print(bool2str("s1" == "s2"));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_008():
    source = """
func main() -> void {
    print(bool2str("s1" != "s2"));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_009():
    source = """
func main() -> void {
    let a: string = "s1" + "s2";
    print(a);
}
"""
    expected = "s1s2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_010():
    source = """
func main() -> void {
    print(bool2str(7 > 5));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_011():
    source = """
func main() -> void {
    print(bool2str(7.5 > 5));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_012():
    source = """
func main() -> void {
    print(bool2str(5.0 >= 5));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_012():
    source = """
func main() -> void {
    print(bool2str(5.0 < 5));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_013():
    source = """
func main() -> void {
    print(int2str(10 % 5));
}
"""
    expected = "0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_014():
    source = """
func main() -> void {
    print(int2str(11 % 3));
}
"""
    expected = "2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_015():
    source = """
func main() -> void {
    let i: int = 3 * 2;
    print(int2str(i));
}
"""
    expected = "6"
    assert CodeGenerator().generate_and_run(source) == expected

def test_016():
    source = """
func main() -> void {
    print(bool2str(true == true));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_017():
    source = """
func main() -> void {
    print(bool2str(true && false));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_018():
    source = """
func main() -> void {
    print(bool2str(true || false));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_019():
    source = """
func main() -> void {
    print(bool2str(!false));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_020():
    source = """
func main() -> void {
    let a: [int;3] = [1,2,3];
    print(int2str(a[0]));
    print(int2str(a[1]));
    print(int2str(a[2]));
}
"""
    expected = "1\n2\n3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_021():
    source = """
func main() -> void {
    let a: [string;2] = ["nguyen", "hieu"];
    print(a[0] + a[1]);
}
"""
    expected = "nguyen hieu"
    assert CodeGenerator().generate_and_run(source) == expected

def test_022():
    source = """
func main() -> void {
    let a: [float;2] = [1.0, 2.0];
    print(float2str(a[0] + a[1]));
}
"""
    expected = "3.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_023():
    source = """
func main() -> void {
    let a: [bool;2] = [true, false];
    print(bool2str(a[0] && a[1]));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_024():
    source = """
func main() -> void {
    let a: [bool;2] = [false, true];
    print(bool2str(a[0] || a[1]));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_025():
    source = """
func main() -> void {
    let a: [[int;2];2] = [[1, 2], [3, 4]];
    print(int2str(a[0][0]));
    print(int2str(a[0][1]));
    print(int2str(a[1][0]));
    print(int2str(a[1][1]));
}
"""
    expected = "1\n2\n3\n4"
    assert CodeGenerator().generate_and_run(source) == expected

def test_026():
    source = """
func main() -> void {
    let a: [[int;2];3] = [[1, 2], [3, 4], [3, 4]];
    /*
    print(int2str(len(a)));
    print(int2str(len(a[0])));
    */
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected

def test_027():
    source = """
func main() -> void {
    let a: [[int;2];3] = [[1, 2], [3, 4], [3, 4]];
    print(int2str(len(a)));
}
"""
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_028():
    source = """
func main() -> void {
    let a: [[int;2];3] = [[1, 2], [3, 4], [3, 4]];
    print(int2str(len(a[0])));
}
"""
    expected = "2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_029():
    source = """
func main() -> void {
    print("s" + 1);
    print("s" + 1.0);
    print("s" + true);
    print("s" + "s");
}
"""
    expected = "s1\ns1.0\nstrue\nss"
    assert CodeGenerator().generate_and_run(source) == expected

def test_030():
    source = """
func main() -> void {
    let a: [int;3] = [1,2,3];
    a[1] = 5;
    print(int2str(a[0]));
    print(int2str(a[1]));
    print(int2str(a[2]));
}
"""
    expected = "1\n5\n3"            
    assert CodeGenerator().generate_and_run(source) == expected


def test_031():
    source = """

func main() -> void {
    print(bool2str(true));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected


def test_032():
    source = """
func foo(a: bool, b: float, c: string) -> void {
    print("" + a + b + c);
}
func main() -> void {
    foo(true, 1.0, "s");
}
"""
    expected = "true1.0s"
    assert CodeGenerator().generate_and_run(source) == expected


def test_033():
    source = """
func foo() -> int {
    return 1;
}
func main() -> void {
    print("" + foo());
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected


def test_034():
    source = """
func foo(a: int) -> int {
    return a;
}
func main() -> void {
    print("" + foo(10));
}

"""
    expected = "10"
    assert CodeGenerator().generate_and_run(source) == expected


def test_035():
    source = """
func foo(arr: [int; 3], value: int) -> int {
    arr[0] = value;
    arr[1] = value * 2;
    arr[2] = value * 3;
    return arr[0] + arr[1] + arr[2];
}
func main() -> void {
    let a: [int;3] = [1,2,3];
    let sum: int = foo(a, 2);
    print("" + a[0] + sum);
}



"""
    expected = "212"
    assert CodeGenerator().generate_and_run(source) == expected


def test_036():
    source = """
func main() -> void {
    let a: [int;3] = [1,2,3];
    let sum: int = foo(a, 2);
    print("" + a[0] + sum);
}
func foo(arr: [int; 3], value: int) -> int {
    arr[0] = value;
    arr[1] = value * 2;
    arr[2] = value * 3;
    return arr[0] + arr[1] + arr[2];
}
"""
    expected = "212"
    assert CodeGenerator().generate_and_run(source) == expected


def test_037():
    source = """
func main() -> void {
    let a: [[int;2];3] = [[1,2],[3,6],[1,8]];
    let sum: int = foo(a, 3);
    print("" + a[0][0] + sum);
}
func foo(arr: [[int;3]; 3], value: int) -> int {
    return arr[1][0] + arr[1][1];
}
"""
    expected = "19"
    assert CodeGenerator().generate_and_run(source) == expected


def test_038():
    source = """
const a = 1;

func main() -> void {
    print("" + a);
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

    
def test_039():
    source = """
func main() -> void {
    let a: int = 5;
    if (a > 3) {
        print(int2str(a));
    }
}
"""
    expected = "5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_040():
    source = """
func main() -> void {
    let a: int = 4;
    if (a > 4) {
        print(int2str(a));
    }
    else {
        print(int2str(a + 1));
    }
}
"""
    expected = "5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_041():
    source = """
func main() -> void{
    let a = 2;
    if (a > 4) {
        print(int2str(a+4));
    }
    else if (a > 1) {
        print(int2str(a + 1));
    }
    else {
        print(int2str(a + 5));
    }
}
"""
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_042():
    source = """
func main() -> void{
    let a = 2;
    if (a > 4) {
        print(int2str(a+4));
    }
    else if (a > 2) {
        print(int2str(a + 1));
    }
    else if (a > 1) {
        let b = 5.6;
        print(float2str(b));
    }
    else {
        print(int2str(a + 5));
    }
}
"""
    expected = "5.6"
    assert CodeGenerator().generate_and_run(source) == expected


def test_042():
    source = """
func main() -> void{
    let a = 2;
    if (a > 4) {
        print(int2str(a+4));
    }
    else if (a > 2) {
        print(int2str(a + 1));
    }
    else if (a > 1) {
        let b = [1.1, 1.2, 1.3, 1.4, 1.5];
        print(float2str(b[4]));
    }
    else {
        print(int2str(a + 5));
    }
}
"""
    expected = "1.5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_042():
    source = """
func main() -> void {
    let a = "0";
    while (true){
        print(a);
        break;
    }
}
"""
    expected = "0"
    assert CodeGenerator().generate_and_run(source) == expected


def test_043():
    source = """
func main() -> void {
    let a = 0;
    while (a < 5){
        print(int2str(a));
        a = a + 1;
    }
}
"""
    expected = "0\n1\n2\n3\n4"
    assert CodeGenerator().generate_and_run(source) == expected


def test_044():
    source = """
func main() -> void {
    let a: int = 0;
    while (a < 6){
        print("" + a);
        if (a == 3) {
            break;
        }
        a = a + 1;
    }
}
"""
    expected = "0\n1\n2\n3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_045():
    source = """
func main() -> void {
    let a = 0;
    while (a < 6){
        print("" + a);
        a = a + 1;
    }
}
"""
    expected = "0\n1\n2\n3\n4\n5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_045():
    source = """
func main() -> void {
    let a = [1, 2, 3, 4, 5, 6, 7];
    for (i in a) {
        print(int2str(i));
    }
}
"""
    expected = "1\n2\n3\n4\n5\n6\n7"
    assert CodeGenerator().generate_and_run(source) == expected


def test_046():
    source = """
const a = [1, 2, 3];
func main() -> void {
    let b = a[a[1]] ;
    print("" + b);
}
"""
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_047():
    source = """
const a = [1, 2, 3];
const b = a[a[1]];
func main() -> void {
    print("" + b);
}
"""
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_048():
    source = """
func main() -> void {
    1;
    return;
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected


def test_049():
    source = """
func foo(a: int) -> void {print("" + a);}
func main() -> void {
    1 >> foo;
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected


def test_050():
    source = """
func foo(a: int, b: int) -> void {print("" + a + b);}
func main() -> void {
    1 >> foo(2);
}
"""
    expected = "12"
    assert CodeGenerator().generate_and_run(source) == expected


def test_051():
    source = """
func main() -> void {
    let a = 1;
    {
        let a = 2;
    }
    print("" + a);
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected


def test_052():
    source = """
func main() -> void {
    let array = [10, 20];
    for (a in array){
        print("" + a);
        break;
        print("" + a);
    }
}
"""
    expected = "10"
    assert CodeGenerator().generate_and_run(source) == expected


def test_053():
    source = """
func main() -> void {
    let array = [10, 20];
    for (a in array){print("" + a);}
    for (a in array){print("" + a);}
}
"""
    expected = "10\n20\n10\n20"
    assert CodeGenerator().generate_and_run(source) == expected


def test_054():
    source = """
func is_odd(n: int) -> bool {
    return n % 2 == 1;
}

func main() -> void {
    let sum = 0;
    let i = 0;

    while (i < 10) {
        i = i + 1;

        if (i == 5) {
            continue;
        }

        if (i == 9) {
            break;
        }

        if (is_odd(i)) {
            sum = sum + i;
        }
    }

    print("Sum is: " + sum);
}
"""
    expected = "Sum is: 11"
    assert CodeGenerator().generate_and_run(source) == expected


def test_055():
    source = """
func main() -> void {
    let a = 10;
    let b = 3;
    let c = 5;
    let d = 2;

    let x = a > b;
    print("x: " + bool2str(x));
}
"""
    expected = (
        "x: true"
    )
    assert CodeGenerator().generate_and_run(source) == expected


def test_056():
    source = """
func main() -> void {
    let a = 10;
    let b = 3;
    let c = 5;
    let d = 2;

    let result1 = a + b * c - d / b + a % d;  // 10 + 3*5 - 2/3 + 10%2

    let cmp1 = a > b && b < c || d == 2;     // true && true || true
    let cmp2 = !(a <= c || b != 3);          // !(false || false)

    let complex = ((a + b) > (c * d)) && ((a % d) == 0) || !(b < d);

    print("result1: " + (result1));
    print("cmp1: " + (cmp1));
    print("cmp2: " + (cmp2));
    print("complex: " + (complex));

    if (result1 > 20 && complex) {
        print("OK1");
    }

    if (cmp1 && !cmp2 || result1 < 50) {
        print("OK2");
    }
}
"""
    expected = (
        "result1: 25\n"
        "cmp1: true\n"
        "cmp2: true\n"
        "complex: true\n"
        "OK1\n"
        "OK2"
    )
    assert CodeGenerator().generate_and_run(source) == expected


def test_057():
    source = """
func main() -> void {
    let i: int = 0;
    while (i < 10) {
        i = i + 1;
        if (i == 5) {
            continue;
        }
        print("" + i);
        
    }
}

"""
    expected = "1\n2\n3\n4\n6\n7\n8\n9\n10"
    assert CodeGenerator().generate_and_run(source) == expected


def test_058():
    source = """
func main() -> void {
    let arr1 = [1, 2, 3];
    let arr2 = arr1;
    arr2[0] = 5;
    for (i in arr1) {
        print("" + i);
    }
}

"""
    expected = "1\n2\n3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_059():
    source = """
func main() -> void {
    let a = [[10, 20], [30, 40]];
    let b = [[1, 2], [3, 4]];
    b[0] = a[0];
    b[0][1] = 2;
    print("" + b[0][1]);
    print("" + a[0][1]);
}
"""
    expected = "2\n20"
    assert CodeGenerator().generate_and_run(source) == expected


def test_060():
    source = """
func main() -> void {
    let a = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ];
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected


def test_061():
    source = """
func main() -> void {
    let a = [
        [1, 2, 3, 4]
    ];
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected


def test_062():
    source = """
func main() -> void {
    let a = [
        [1]
    ];
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected


def test_063():
    source = """
func main() -> void {
    let a = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ];
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected


def test_064():
    source = """
func main() -> void {
    let a = [
        [1, 2, 3, 4]
    ];
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected


def test_065():
    source = """
func main() -> void {
    let a = [
        [1]
    ];
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected


def test_066():
    source = """
func main() -> void {
    let a: [[int;2];3] = [[1, 2], [3, 4], [5, 6]];
    a[0] = a[1];
    print("" + a[0][0] + a[0][1]);
}
"""
    expected = "34"
    assert CodeGenerator().generate_and_run(source) == expected


def test_067():
    source = """
func main() -> void {
    let nums: [int;5] = [1, 2, 3, 4, 5];
    let sum: int = 0;
    for (num in nums) {
        sum = sum + num;
    }
    print(int2str(sum));
}
"""
    expected = "15"
    assert CodeGenerator().generate_and_run(source) == expected

def test_068():
    source = """
func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
func main() -> void {
    print(int2str(factorial(5)));
}
"""
    expected = "120"
    assert CodeGenerator().generate_and_run(source) == expected

def test_069():
    source = """
func main() -> void {
    let str1: string = "test";
    let str2: string = "test";
    let str3: string = "demo";
    print(bool2str(str1 == str2));
    print(bool2str(str1 == str3));
}
"""
    expected = "true\nfalse"
    assert CodeGenerator().generate_and_run(source) == expected

def test_070():
    source = """
func main() -> void {
    let arr: [int;1] = [42];
    print(int2str(len(arr)));
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_071():
    source = """
func main() -> void {
    let a: float = 10.0;
    let b: float = 3.0;
    print(float2str(a + b));
    print(float2str(a - b));
}
"""
    expected = "13.0\n7.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_072():
    source = """
func main() -> void {
    let flag: bool = false;
    if (!flag) {
        print("Not false");
    }
}
"""
    expected = "Not false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_073():
    source = """
func main() -> void {
    let values: [string;3] = ["a", "b", "c"];
    for (val in values) {
        print(val);
    }
}
"""
    expected = "a\nb\nc"
    assert CodeGenerator().generate_and_run(source) == expected

def test_074():
    source = """
func doubleValue(x: int) -> int {
    return x * 2;
}
func main() -> void {
    let result: int = doubleValue(5);
    print(int2str(result));
}
"""
    expected = "10"
    assert CodeGenerator().generate_and_run(source) == expected

def test_075():
    source = """
func main() -> void {
    let matrix: [[string;2];2] = [["a", "b"], ["c", "d"]];
    print(matrix[0][0] + matrix[1][1]);
}
"""
    expected = "ad"
    assert CodeGenerator().generate_and_run(source) == expected

def test_076():
    source = """
const MESSAGE: string = "Hello";
func main() -> void {
    print(MESSAGE + " Constant");
}
"""
    expected = "Hello Constant"
    assert CodeGenerator().generate_and_run(source) == expected

def test_077():
    source = """
func main() -> void {
    let i: int = 0;
    while (i < 3) {
        if (i == 1) {
            i = i + 1;
            continue;
        }
        print(int2str(i));
        i = i + 1;
    }
}
"""
    expected = "0\n2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_078():
    source = """
func main() -> void {
    let x: int = 10;
    let y: int = 3;
    print(int2str(x % y));
    print(int2str(x / y));
}
"""
    expected = "1\n3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_079():
    source = """
func add(a: int, b: int) -> int {
    return a + b;
}
func main() -> void {
    let result: int = add(15, 25);
    print(int2str(result));
}
"""
    expected = "40"
    assert CodeGenerator().generate_and_run(source) == expected

def test_080():
    source = """
func main() -> void {
    let bools: [bool;3] = [true, false, true];
    for (b in bools) {
        print(bool2str(b));
    }
}
"""
    expected = "true\nfalse\ntrue"
    assert CodeGenerator().generate_and_run(source) == expected

def test_081():
    source = """
func main() -> void {
    let matrix: [[int;2];2] = [[1, 2], [3, 4]];
    print(int2str(matrix[0][0]));
    print(int2str(matrix[1][1]));
}
"""
    expected = "1\n4"
    assert CodeGenerator().generate_and_run(source) == expected

def test_082():
    source = """
func main() -> void {
    let str: string = "Test string with spaces";
    print(str);
}
"""
    expected = "Test string with spaces"
    assert CodeGenerator().generate_and_run(source) == expected

def test_083():
    source = """
func max(a: int, b: int) -> int {
    if (a > b) {
        return a;
    }
    return b;
}
func main() -> void {
    print(int2str(max(7, 12)));
}
"""
    expected = "12"
    assert CodeGenerator().generate_and_run(source) == expected

def test_084():
    source = """
func main() -> void {
    let floats: [float;2] = [1.5, 2.5];
    let sum: float = floats[0] + floats[1];
    print(float2str(sum));
}
"""
    expected = "4.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_085():
    source = """
func main() -> void {
    let x: int = 5;
    {
        let y: int = 10;
        print(int2str(x + y));
    }
    print(int2str(x));
}
"""
    expected = "15\n5"
    assert CodeGenerator().generate_and_run(source) == expected

def test_086():
    source = """
func isPositive(num: int) -> bool {
    return num > 0;
}
func main() -> void {
    print(bool2str(isPositive(5)));
    print(bool2str(isPositive(-3)));
}
"""
    expected = "true\nfalse"
    assert CodeGenerator().generate_and_run(source) == expected

def test_087():
    source = """
func main() -> void {
    let chars: [string;4] = ["A", "B", "C", "D"];
    print(chars[1] + chars[3]);
}
"""
    expected = "BD"
    assert CodeGenerator().generate_and_run(source) == expected

def test_088():
    source = """
const PI: float = 3.14;
func area(radius: float) -> float {
    return PI * radius * radius;
}
func main() -> void {
    print(float2str(area(2.0)));
}
"""
    expected = "12.56"
    assert CodeGenerator().generate_and_run(source) == expected

def test_089():
    source = """
func main() -> void {
    let count: int = 0;
    while (count < 5) {
        count = count + 1;
        if (count == 3) {
            break;
        }
    }
    print(int2str(count));
}
"""
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_090():
    source = """
func processString(s: string) -> void {
    print("Processing: " + s);
}
func main() -> void {
    processString("hello");
}
"""
    expected = "Processing: hello"
    assert CodeGenerator().generate_and_run(source) == expected

def test_091():
    source = """
func main() -> void {
    let a: bool = true;
    let b: bool = false;
    print(bool2str(a || b));
    print(bool2str(a && b));
}
"""
    expected = "true\nfalse"
    assert CodeGenerator().generate_and_run(source) == expected

def test_092():
    source = """
func main() -> void {
    let nums: [int;4] = [10, 20, 30, 40];
    nums[2] = 99;
    for (n in nums) {
        print(int2str(n));
    }
}
"""
    expected = "10\n20\n99\n40"
    assert CodeGenerator().generate_and_run(source) == expected

def test_093():
    source = """
func main() -> void {
    let x: float = 7.5;
    let y: float = 2.5;
    let result: bool = x >= y;
    print(bool2str(result));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_094():
    source = """
func main() -> void {
    let table: [[float;2];3] = [[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]];
    print(float2str(table[1][0]));
}
"""
    expected = "3.3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_095():
    source = """
func main() -> void {
    let str1: string = "Part1";
    let str2: string = "Part2";
    let combined: string = str1 + str2;
    print(combined);
}
"""
    expected = "Part1Part2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_096():
    source = """
func main() -> void {
    let i: int = 0;
    while (i < 10) {
        i = i + 1;
        if (i % 2 == 0) {
            continue;
        }
        if (i > 5) {
            break;
        }
        print(int2str(i));
    }
}
"""
    expected = "1\n3\n5"
    assert CodeGenerator().generate_and_run(source) == expected

def test_097():
    source = """
func power(base: int, exp: int) -> int {
    if (exp == 0) {
        return 1;
    }
    return base * power(base, exp - 1);
}
func main() -> void {
    print(int2str(power(2, 4)));
}
"""
    expected = "16"
    assert CodeGenerator().generate_and_run(source) == expected

def test_098():
    source = """
func main() -> void {
    let values: [bool;4] = [true, false, true, false];
    let trueCount: int = 0;
    for (val in values) {
        if (val) {
            trueCount = trueCount + 1;
        }
    }
    print(int2str(trueCount));
}
"""
    expected = "2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_099():
    source = """
func main() -> void {
    let grid: [[string;2];2] = [["X", "O"], ["O", "X"]];
    for (row in grid) {
        for (cell in row) {
            print(cell);
        }
    }
}
"""
    expected = "X\nO\nO\nX"
    assert CodeGenerator().generate_and_run(source) == expected

def test_100():
    source = """
func calculate(a: float, b: float) -> float {
    return a * b;
}
func main() -> void {
    print(float2str(calculate(10.0, 3.0)));
}
"""
    expected = "30.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_101():
    source = """
const NUMBERS: [int;5] = [2, 4, 6, 8, 10];
func sum(arr: [int;5]) -> int {
    let total: int = 0;
    for (num in arr) {
        total = total + num;
    }
    return total;
}
func main() -> void {
    let result: int = sum(NUMBERS);
    print("Sum is: " + int2str(result));
}
"""
    expected = "Sum is: 30"
    assert CodeGenerator().generate_and_run(source) == expected