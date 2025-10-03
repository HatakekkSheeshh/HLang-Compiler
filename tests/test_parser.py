from utils import Parser


def test_001():
    """Test basic function declaration"""
    source = """func main() -> void {}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_002():
    """Test function with parameters"""
    source = """func add(a: int, b: int) -> int { return a + b; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    """Test variable declaration with type annotation"""
    source = """func main() -> void { let x: int = 42; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_004():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice"; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test constant declaration"""
    source = """const PI: float = 3.14159; func main() -> void {}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """func main() -> void { 
        if (x > 0) { 
            print("positive"); 
        } else { 
            print("negative"); 
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test while loop"""
    source = """func main() -> void { 
        let i = 0;
        while (i < 10) { 
            i = i + 1; 
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with array"""
    source = """func main() -> void { 
        let numbers = [1, 2, 3, 4, 5];
        for (num in numbers) { 
            print(str(num)); 
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """func main() -> void { 
        let arr: [int; 3] = [1, 2, 3];
        let first = arr[0];
        arr[1] = 42;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test complex expression with pipeline operator"""
    source = """func main() -> void { 
        let result = data >> process >> validate >> transform;
        let calculation = 5 >> add(3) >> multiply(2);
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_011():
    """Test empty array literal"""
    source = """const a = [];
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected

         
def test_012():
    """Test nested array of integers"""
    source = """const matrix = [[1, 2], [3, 4], [5, 6]];
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_013():
    """Test nested array of integers"""
    source = """const matrix = [[[1, 2], [3, 4], [5, 6]], [[1, 2], [3, 4], [5, 6]]];
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_014():
    """Test array literal"""
    source = """const words = [1, [], "three"];
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_015():
    """Test nested nested... array literal"""
    source = """const words = [1, [], "hieu", [[]], [[1,2,3,4,5]]];
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_016():
    """Test array literal"""
    source = """const quochieu = [1, ];
    """
    expected = "Error on line 1 col 21: ]"
    assert Parser(source).parse() == expected


def test_017():
    source = """const cr7 = -(+a);
    func main() -> void {}
    """
    assert Parser(source).parse() == "success"


def test_018():
    source = '''const pepsi = a[1] + a[1+1] + c["s" * c];
    func main() -> void {}
    '''
    assert Parser(source).parse() == "success"


def test_019():
    source = """const cocacola = arr[1][a[2] + 1];
    func main() -> void {}
    """
    assert Parser(source).parse() == "success"


def test_020():
    source = """const haha = [1, 2][2][2+2][3];
    func main() -> void {}
    """
    assert Parser(source).parse() == "success"

def test_021():
    source = "const array = [1, 2][2, [3,4,5], [7,8]][2+2][3];"
    assert Parser(source).parse() == "Error on line 1 col 22: ,"

def test_022():
    source = """const var = (1+2)*3 + (a)[2][3];
    func main() -> void {}
    """
    assert Parser(source).parse() == "success"

def test_023():
    source = """const array = a[];
    func main() -> void {}
    """
    assert Parser(source).parse() == "Error on line 1 col 16: ]"


def test_024():
    source = """const array = a[1, 2];
    func main() -> void {}
    """
    assert Parser(source).parse() == "Error on line 1 col 17: ,"


def test_025():
    source = """const var = foo()[2][3] + 3[2];
    func main() -> void {}
    """
    assert Parser(source).parse() == "success"


def test_026():
    source = """const funct = str() + int(2, 3) + int(2) + int() + float() + float(true * 2);
    func main() -> void {}
    """
    assert Parser(source).parse() == "success"


def test_027():
    source = '''
    const a1 = 123;
    const a2: int = 456;
    const b1 = 3.14;
    const b2: float = 2.71;
    const c1 = true;
    const c2: bool = false;
    const d1 = "hello";
    const d2: string = "world";
    const e1 = [1, 2, 3];
    const e2: [int; 3] = [4, 5, 6];
    func main() -> void {}
    '''       
    assert Parser(source).parse() == "success"


def test_028():
    source = '''
        const e2: [[[int;1];2]; 3] = 1;
        func main() -> void {}
    '''
    assert Parser(source).parse() == "success"


def test_029():
    source = '''
        const e2: void = 1;
        func main() -> void {}
    '''
    assert Parser(source).parse() == "Error on line 2 col 18: void"


def test_030():
    source = '''
    func f1() -> void {}
    func f2(a: int) -> int {}
    func f3(x: int, y: float, z: string) -> string {}
    func f4(arr: [int; 3]) -> [int; 3] {}
    func f5() -> bool {}
    func f6() -> float {}
    func empty() -> int {}
    '''
    assert Parser(source).parse() == "success"


def test_031():
    source = '''
    func main () -> void {
        1 + 1;
        a[2];
        foo(1,2)[2][3] + foo()[2] + foo();
        a >> 2;
        a >= 1 <= 2 && c;
        int(1) + int(1,2) + float();
        print();
    }
    '''
    assert Parser(source).parse() == "success"


def test_032():
    source = '''
    func main () -> void {
        foo()[2] = 1;
    }
    '''
    assert Parser(source).parse() == "Error on line 3 col 17: ="


def test_033():
    source = '''
    func main () -> void {
    let b :string = 1;
    let b  = 1 + 1;
    let b :[int;1] = b;
    }
    '''
    assert Parser(source).parse() == "success"


def test_034():
    """Test parser error: missing closing brace in function declaration"""
    source = """func main() -> void { let x = 1; """  # Thiếu dấu }
    expected = "Error on line 1 col 33: <EOF>"
    assert Parser(source).parse() == expected

def test_035():
    source = """
    const a = string();
    func main() -> void {}
    """
    expected = "Error on line 2 col 14: string"
    assert Parser(source).parse() == expected

def test_036():
    """Blank"""
    source = """
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_037():
    source = """
    func test() -> int {
        return 42;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_038():
    source = """
    func fibonacci(n: int) -> int {
        if (n <= 1) {
            return n;
        }
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_039():
    source = """
    func main() -> void {
        let arr: [int; 5] = [1, 2, 3, 4, 5];
        for (item in arr) {
            print(str(item));
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_040():
    source = """
    func main() -> void {
        let x = 10;
        while (x > 0) {
            x = x - 1;
            if (x == 5) {
                break;
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_041():
    source = """
    func main() -> void {
        let result = 5 >> add(3) >> multiply(2) >> subtract(1);
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_042():
    source = """
    const PI: float = 3.14159;
    const NAME: string = "HLang";
    const ENABLED: bool = true;
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_043():
    source = """
    func main() -> void {
        let matrix: [[int; 3]; 3] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
        let element = matrix[1][2];
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_044():
    source = """
    func main() -> void {
        let a = 5;
        let b = 10;
        if (a > b) {
            print("a is greater");
        } else if (a < b) {
            print("b is greater");
        } else {
            print("they are equal");
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_045():
    source = """
    func calculate(x: int, y: int) -> int {
        return x * y + (x - y) / 2;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_046():
    source = """
    func main() -> void {
        let numbers = [1, 2, 3, 4, 5];
        numbers[0] = 10;
        numbers[1] = numbers[0] + 5;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_047():
    source = """
    func main() -> void {
        let condition = true && false || !true;
        let comparison = 5 > 3 && 2 <= 4;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_048():
    source = """
    func main() -> void {
        let str_result = "Hello" + " " + "World";
        let num_result = 10 + 20 * 3 - 5 / 2;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_049():
    source = """
    func main() -> void {
        {
            let local_var = 42;
            {
                let inner_var = local_var * 2;
                print(str(inner_var));
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_050():
    source = """
    func main() -> void {
        for (i in [1, 2, 3, 4, 5]) {
            if (i % 2 == 0) {
                continue;
            }
            print(str(i));
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_051():
    source = """
    func main() -> void {
        let empty_array: [int; 0] = [];
        let mixed_array = [1, 2, 3, [], [4, 5]];
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_052():
    source = """
    func main() -> void {
        let result = func_call() + another_func(1, 2, 3);
        let chained = obj.method().another_method();
    }
    """
    expected = "Error on line 4 col 25: ."
    assert Parser(source).parse() == expected


def test_053():
    source = """
    func main() -> void {
        let x = -(-5);
        let y = !(!true);
        let z = +(+42);
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_054():
    source = """
    func main() -> void {
        return;
    }
    func test() -> int {
        return 42;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_055():
    source = """
    func main() -> void {
        let arr = [1, 2, 3];
        arr[0] = arr[1] + arr[2];
        let multi_dim = [[1, 2], [3, 4]];
        multi_dim[0][1] = 5;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_056():
    source = """
    func main() -> void {
        let x = 5;
        let y = (x + 3) * (x - 1);
        let z = ((x + y) / 2) % 3;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_057():
    source = """
    func main() -> void {
        let data = [1, 2, 3, 4, 5];
        let processed = data >> filter(is_even) >> map(double) >> sum();
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_058():
    source = """
    func main() -> void {
        let str_lit = "Hello, World!";
        let escaped = "Line 1\nLine 2\tTabbed";
        let quoted = "She said \"Hello\"";
    }
    """
    expected = "Unclosed String: Line 1\n"
    assert Parser(source).parse() == expected


def test_059():
    source = """
    func main() -> void {
        let float_num = 3.14159;
        let scientific = 1.23e-4;
        let another = 2.5e+3;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_060():
    source = """
    const MAX_SIZE: int = 100;
    func process_array(arr: [int; MAX_SIZE]) -> [int; MAX_SIZE] {
        return arr;
    }
    """
    expected = "Error on line 3 col 34: MAX_SIZE"
    assert Parser(source).parse() == expected


def test_061():
    source = """
    func main() -> void {
        let x = 5;
        if (x > 0) {
            if (x > 10) {
                print("large");
            } else {
                print("small positive");
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_062():
    source = """
    func main() -> void {
        let counter = 0;
        while (counter < 10) {
            counter = counter + 1;
            if (counter == 5) {
                continue;
            }
            print(str(counter));
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_063():
    source = """
    func main() -> void {
        let arr = [1, 2, 3, 4, 5];
        for (num in arr) {
            if (num > 3) {
                break;
            }
            print(str(num));
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_064():
    source = """
    func add(a: int, b: int) -> int {
        return a + b;
    }
    func multiply(x: int, y: int) -> int {
        return x * y;
    }
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_065():
    source = """
    func main() -> void {
        let result = 10 + 20 * 30 / 4 - 5 % 2;
        let logical = true && false || !true;
        let comparison = 5 >= 3 && 2 != 4;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_066():
    source = """
    func main() -> void {
        let x = 5;
        x = x + 1;
        x = x * 2;
        x = x / 3;
        x = x % 4;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_067():
    source = """
    func main() -> void {
        let arr: [int; 3] = [1, 2, 3];
        let first = arr[0];
        let last = arr[arr.length - 1];
    }
    """
    expected = "Error on line 5 col 26: ."
    assert Parser(source).parse() == expected


def test_068():
    source = """
    func main() -> void {
        let numbers = [1, 2, 3, 4, 5];
        let sum = 0;
        for (num in numbers) {
            sum = sum + num;
        }
        print(str(sum));
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_069():
    source = """
    func factorial(n: int) -> int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_070():
    source = """
    func main() -> void {
        let matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
        for (row in matrix) {
            for (element in row) {
                print(str(element));
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_071():
    source = """
    func main() -> void {
        let condition = true;
        let result = condition ? "yes" : "no";
    }
    """
    expected = "Error Token ?"
    assert Parser(source).parse() == expected


def test_072():
    source = """
    func main() -> void {
        let x = 10;
        switch (x) {
            case 1: print("one"); break;
            case 2: print("two"); break;
            default: print("other");
        }
    }
    """
    expected = "Error on line 4 col 19: {"
    assert Parser(source).parse() == expected


def test_073():
    source = """
    func main() -> void {
        let arr = [1, 2, 3, 4, 5];
        let filtered = arr.filter(x => x > 3);
    }
    """
    expected = "Error on line 4 col 26: ."
    assert Parser(source).parse() == expected


def test_074():
    source = """
    func main() -> void {
        let x = 5;
        let y = ++x;
        let z = x--;
    }
    """
    expected = "Error on line 5 col 19: ;"
    assert Parser(source).parse() == expected


def test_075():
    source = """
    func main() -> void {
        let obj = {
            name: "John",
            age: 30,
            city: "New York"
        };
    }
    """
    expected = "Error on line 3 col 18: {"
    assert Parser(source).parse() == expected


def test_076():
    source = """
    func main() -> void {
        let x = 5;
        let y = x += 3;
    }
    """
    expected = "Error on line 4 col 19: ="
    assert Parser(source).parse() == expected


def test_077():
    source = """
    func main() -> void {
        let arr = [1, 2, 3];
        let [first, second, third] = arr;
    }
    """
    expected = "Error on line 4 col 12: ["
    assert Parser(source).parse() == expected


def test_078():
    source = """
    func main() -> void {
        let x = 5;
        let y = x ** 2;
    }
    """
    expected = "Error on line 4 col 19: *"
    assert Parser(source).parse() == expected


def test_079():
    source = """
    func main() -> void {
        let str = "Hello";
        let interpolated = `Hello ${name}!`;
    }
    """
    expected = "Error Token `"
    assert Parser(source).parse() == expected


def test_080():
    source = """
    func main() -> void {
        let x = 5;
        let y = x?.value;
    }
    """
    expected = "Error Token ?"
    assert Parser(source).parse() == expected


def test_081():
    source = """
    func main() -> void {
        let arr = [1, 2, 3, 4, 5];
        let sliced = arr[1:3];
    }
    """
    expected = "Error on line 4 col 26: :"
    assert Parser(source).parse() == expected


def test_082():
    source = """
    func main() -> void {
        let x = 5;
        let y = x ?? 10;
    }
    """
    expected = "Error Token ?"
    assert Parser(source).parse() == expected


def test_083():
    source = """
    func main() -> void {
        let arr = [1, 2, 3];
        let spread = [...arr, 4, 5];
    }
    """
    expected = "Error on line 4 col 22: ."
    assert Parser(source).parse() == expected


def test_084():
    source = """
    func main() -> void {
        let x = 5;
        x *= 3;
        x /= 2;
        x %= 4;
    }
    """
    expected = "Error on line 4 col 11: ="
    assert Parser(source).parse() == expected


def test_085():
    source = """
    func main() -> void {
        let regex = /[a-z]+/g;
        let match = "hello".match(regex);
    }
    """
    expected = "Error on line 3 col 20: /"
    assert Parser(source).parse() == expected


def test_086():
    source = """
    func main() -> void {
        let x = 5;
        let y = x <=> 10;
    }
    """
    expected = "Error on line 4 col 20: >"
    assert Parser(source).parse() == expected


def test_087():
    source = """
    func main() -> void {
        let arr = [1, 2, 3];
        for (let i = 0; i < arr.length; i++) {
            print(str(arr[i]));
        }
    }
    """
    expected = "Error on line 4 col 13: let"
    assert Parser(source).parse() == expected


def test_088():
    source = """
    func main() -> void {
        let x = 5;
        let y = x & 3;
    }
    """
    expected = "Error Token &"
    assert Parser(source).parse() == expected


def test_089():
    source = """
    func main() -> void {
        let x = 5;
        let y = x << 2;
        let z = x >> 1;
    }
    """
    expected = "Error on line 4 col 19: <"
    assert Parser(source).parse() == expected


def test_090():
    source = """
    func main() -> void {
        let x = 5;
        let y = ~x;
    }
    """
    expected = "Error Token ~"
    assert Parser(source).parse() == expected


def test_091():
    source = """
    func main() -> void {
        let x = 5;
        let y = x instanceof Number;
    }
    """
    expected = "Error on line 4 col 18: instanceof"
    assert Parser(source).parse() == expected


def test_092():
    source = """
    func main() -> void {
        let x = 5;
        let y = typeof x;
    }
    """
    expected = "Error on line 4 col 23: x"
    assert Parser(source).parse() == expected


def test_093():
    source = """
    func main() -> void {
        let x = 5;
        return x;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_094():
    source = """
    func main() -> void {
        let x = 5;
        let y = x in [1, 2, 3, 4, 5];
    }
    """
    expected = "Error on line 4 col 18: in"
    assert Parser(source).parse() == expected


def test_095():
    source = """
    func main() -> void {
        let x = 5;
        let y = x * "string";
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_096():
    source = """
    func main() -> void {
        let x = 5;
        let y = x is int;
    }
    """
    expected = "Error on line 4 col 18: is"
    assert Parser(source).parse() == expected


def test_097():
    source = """
    func main() -> void {
        let x = 5;
        let y = x.toString();
    }
    """
    expected = "Error on line 4 col 17: ."
    assert Parser(source).parse() == expected


def test_098():
    source = """
    func main() -> void {
        let Class = class; 
        {
            constructor();
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_099():
    source = """
    func main() -> void {
        let x = 5;
        let y = new Array(10);
    }
    """
    expected = "Error on line 4 col 20: Array"
    assert Parser(source).parse() == expected


def test_100():
    source = """
    func try() -> void {
        let x = 1 / 0;
    } 
    func catch(e: int) -> void {
        print("Error occurred");
    }
    func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected 

def test_101():
    source = """
    const array = [1, 2][[2,4,5]];
    """
    expected = "success"
    assert Parser(source).parse() == expected 


def test_102():
    """Test complex array literal with expressions"""
    source = """func main() -> void {
        let arr = [x + 1, y * 2, func(z), [1, 2, 3]];
    }"""
    expected = "Error on line 2 col 33: func"
    assert Parser(source).parse() == expected


def test_103():
    """Test error: missing closing bracket in array type"""
    source = """func test(arr: [int; 5] -> void {}"""
    expected = "Error on line 1 col 24: ->"
    assert Parser(source).parse() == expected


def test_104():
    """Test error: missing closing bracket in array type"""
    source = """func test(arr: [int; 5) -> void {}"""
    expected = "Error on line 1 col 22: )"
    assert Parser(source).parse() == expected


def test_105():
    """Test expression statement with function call"""
    source = """func main() -> void {
        print("hello");
        calculate(x, y, z);
        obj()[key];
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_106():
    """Test error: missing closing parenthesis in function call"""
    source = """func main() -> void {
        process(a, b;
    }"""
    expected = "Error on line 2 col 20: ;"
    assert Parser(source).parse() == expected