from utils import Tokenizer


def test_000():
    """Test basic identifier tokenization"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_001():
    """Test keywords recognition"""
    source = "func main if else while for let const"
    expected = "func,main,if,else,while,for,let,const,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    """Test integer literals"""
    source = "42 0 -17 007"
    expected = "42,0,-,17,007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    """Test float literals"""
    source = "3.14 -2.5 0.0 42. 5."
    expected = "3.14,-,2.5,0.0,42.,5.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_004():
    """Test boolean literals"""
    source = "true false"
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_005():
    """Test unclosed string literal error"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_006():
    """Test illegal escape sequence error"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_007():
    """Test error character (non-ASCII or invalid character)"""
    source = "let x = 5; @ invalid"
    expected = "let,x,=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_008():
    """Test valid string literals with escape sequences"""
    source = '"Hello World" "Line 1\\nLine 2" "Quote: \\"text\\""'
    expected = "Hello World,Line 1\\nLine 2,Quote: \\\"text\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009():
    """Test string literals return content without quotes"""
    source = '"Hello World"'
    expected = "Hello World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_010():
    """Test empty string literal"""
    source = '""'
    expected = ",EOF"  # Empty string content
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_011():
    """Test operators and separators"""
    source = "+ - * / % == != < <= > >= && || ! = -> >> ( ) [ ] { } , ; :"
    expected = "+,-,*,/,%,==,!=,<,<=,>,>=,&&,||,!,=,->,>>,(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_012():
    """Test identifiers with underscore"""
    source = "_abc abc_ _123 _"
    expected = "_abc,abc_,_123,_,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_013():
    """Test type keywords"""
    source = "int float bool string void"
    expected = "int,float,bool,string,void,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_014():
    """Test control flow keywords"""
    source = "break continue return"
    expected = "break,continue,return,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_015():
    """Test for loop keyword"""
    source = "for in"
    expected = "for,in,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_016():
    """Test large integer literals"""
    source = "123456789 999999999"
    expected = "123456789,999999999,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_017():
    """Test scientific notation floats"""
    source = "1.23e10 1.23E-10 1.e5 1.E-5"
    expected = "1.23e10,1.23E-10,1.e5,1.E-5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_018():
    """Test float with trailing zeros"""
    source = "3.1400 2.5000 0.1000"
    expected = "3.1400,2.5000,0.1000,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_019():
    """Test string with all escape sequences"""
    source = '"\\b\\t\\n\\r\\"\\\\"'
    expected = "Illegal Escape In String: \\b"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_020():
    """Test string with mixed content"""
    source = '"Hello\\nWorld\\tTab\\rReturn"'
    expected = "Hello\\nWorld\\tTab\\rReturn,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_021():
    """Test complex identifiers"""
    source = "myVariable123 _privateVar camelCase snake_case"
    expected = "myVariable123,_privateVar,camelCase,snake_case,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_022():
    """Test unclosed string with newline"""
    source = '"Hello\nWorld"'
    expected = "Unclosed String: Hello\n" 
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_023():
    """Test unclosed string with carriage return"""
    source = '"Hello\r\nWorld"'
    expected = "Unclosed String: Hello\r\n"  
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_024():
    """Test illegal escape with x"""
    source = '"Hello\\xWorld"'
    expected = "Illegal Escape In String: Hello\\x"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_025():
    """Test illegal escape with y"""
    source = '"Hello\\yWorld"'
    expected = "Illegal Escape In String: Hello\\y"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_026():
    """Test illegal escape with z"""
    source = '"Hello\\zWorld"'
    expected = "Illegal Escape In String: Hello\\z"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_027():
    """Test error character hash"""
    source = "let x = 5; # comment"
    expected = "let,x,=,5,;,Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_028():
    """Test error character dollar"""
    source = "let x = $5;"
    expected = "let,x,=,Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_029():
    """Test error character ampersand"""
    source = "let x = 5 & y;"
    expected = "let,x,=,5,Error Token &"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_030():
    """Test error character pipe"""
    source = "let x = 5 | y;"
    expected = "let,x,=,5,Error Token |"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_031():
    """Test error character tilde"""
    source = "let x = ~5;"
    expected = "let,x,=,Error Token ~"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_032():
    """Test error character caret"""
    source = "let x = 5 ^ 3;"
    expected = "let,x,=,5,Error Token ^"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_033():
    """Test error character question mark"""
    source = "let x = 5 ? 3 : 4;"
    expected = "let,x,=,5,Error Token ?"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_034():
    """Test error character backtick"""
    source = "let x = `hello`;"
    expected = "let,x,=,Error Token `"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_035():
    """Test error character at symbol"""
    source = "let x = @variable;"
    expected = "let,x,=,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_036():
    """Test error character percent in wrong context"""
    source = "let x = %5;"
    expected = "let,x,=,%,5,;,EOF"  # % là operator MOD
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_037():
    """Test multiple error characters"""
    source = "let x = @#$%^&*();"
    expected = "let,x,=,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_038():
    """Test string với escape không hợp lệ"""
    source = '"\\n\\t\\r\\b"'
    expected = "Illegal Escape In String: \\n\\t\\r\\b"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_039():
    """Test string with quotes inside"""
    source = '"He said \\"Hello\\" to me"'
    expected = "He said \\\"Hello\\\" to me,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_040():
    """Test string with backslash inside"""
    source = '"Path: C:\\\\Users\\\\Name"'
    expected = "Path: C:\\\\Users\\\\Name,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_041():
    """Test string with mixed escape and normal characters"""
    source = '"Hello\\nWorld\\tTab\\rReturn\\bBackspace"'
    expected = "Illegal Escape In String: Hello\\nWorld\\tTab\\rReturn\\b"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_042():
    """Test float with positive exponent"""
    source = "1.23e+10 2.5E+5"
    expected = "1.23e+10,2.5E+5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_043():
    """Test float with negative exponent"""
    source = "1.23e-10 2.5E-5"
    expected = "1.23e-10,2.5E-5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_044():
    """Test float without decimal part"""
    source = "1.e5 2.E-3 3.e+7"
    expected = "1.e5,2.E-3,3.e+7,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_045():
    """Test float with decimal but no exponent"""
    source = "3.14159 2.71828 1.41421"
    expected = "3.14159,2.71828,1.41421,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_046():
    """Test float with trailing decimal"""
    source = "5. 10. 100."
    expected = "5.,10.,100.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_047():
    """Test integer with leading zeros"""
    source = "007 00123 0000"
    expected = "007,00123,0000,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_048():
    """Test zero in different forms"""
    source = "0 00 000 0.0 0.00"
    expected = "0,00,000,0.0,0.00,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_049():
    """Test negative numbers"""
    source = "-42 -3.14 -0.5 -100"
    expected = "-,42,-,3.14,-,0.5,-,100,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_050():
    """Test large negative numbers"""
    source = "-999999999 -123456789"
    expected = "-,999999999,-,123456789,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_051():
    """Test identifiers starting with underscore"""
    source = "_variable _123 _private _public"
    expected = "_variable,_123,_private,_public,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_052():
    """Test identifiers with numbers"""
    source = "var1 var2 var123 variable123"
    expected = "var1,var2,var123,variable123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_053():
    """Test identifiers with mixed case"""
    source = "camelCase PascalCase snake_case UPPER_CASE"
    expected = "camelCase,PascalCase,snake_case,UPPER_CASE,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_054():
    """Test single character identifiers"""
    source = "a b c x y z"
    expected = "a,b,c,x,y,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_055():
    """Test long identifiers"""
    source = "veryLongVariableName extremelyLongIdentifierName"
    expected = "veryLongVariableName,extremelyLongIdentifierName,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_056():
    """Test operators in sequence"""
    source = "++--**//%%"
    expected = "+,+,-,-,*,*,EOF"  # // và %% bị bỏ qua bởi comment rules
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_057():
    """Test comparison operators"""
    source = "== != < <= > >="
    expected = "==,!=,<,<=,>,>=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_058():
    """Test logical operators"""
    source = "&& || !"
    expected = "&&,||,!,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_059():
    """Test assignment and arrow operators"""
    source = "= -> >>"
    expected = "=,->,>>,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_060():
    """Test separators"""
    source = "() [] {} , ; : ."
    expected = "(,),[,],{,},,,;,:,.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_061():
    """Test mixed operators and separators"""
    source = "(a + b) * [c - d]"
    expected = "(,a,+,b,),*,[,c,-,d,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_062():
    """Test string with newline escape"""
    source = '"Line 1\\nLine 2"'
    expected = "Line 1\\nLine 2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_063():
    """Test string with tab escape"""
    source = '"Column1\\tColumn2\\tColumn3"'
    expected = "Column1\\tColumn2\\tColumn3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_064():
    """Test string with carriage return escape"""
    source = '"Old\\rNew"'
    expected = "Old\\rNew,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_065():
    """Test string with backspace escape"""
    source = '"Hello\\bWorld"'
    expected = "Illegal Escape In String: Hello\\b"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_066():
    """Test string with quote escape"""
    source = '"He said \\"Hello\\" to me"'
    expected = "He said \\\"Hello\\\" to me,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_067():
    """Test string with backslash escape"""
    source = '"Path: C:\\\\Users"'
    expected = "Path: C:\\\\Users,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_068():
    """Test unclosed string at EOF"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_069():
    """Test unclosed string with newline"""
    source = '"Hello\n'
    expected = "Unclosed String: Hello\n"  # Error message bao gồm newline
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_070():
    """Test unclosed string with carriage return"""
    source = '"Hello\\r'
    expected = "Unclosed String: Hello\\r"  # Error message bao gồm carriage return
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_071():
    """Test illegal escape with a"""
    source = '"Hello\\aWorld"'
    expected = "Illegal Escape In String: Hello\\a"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_072():
    """Test illegal escape with c"""
    source = '"Hello\\cWorld"'
    expected = "Illegal Escape In String: Hello\\c"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_073():
    """Test illegal escape with d"""
    source = '"Hello\\dWorld"'
    expected = "Illegal Escape In String: Hello\\d"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_074():
    """Test illegal escape with e"""
    source = '"Hello\\eWorld"'
    expected = "Illegal Escape In String: Hello\\e"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_075():
    """Test illegal escape with f"""
    source = '"Hello\\fWorld"'
    expected = "Illegal Escape In String: Hello\\f"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_076():
    """Test illegal escape with g"""
    source = '"Hello\\gWorld"'
    expected = "Illegal Escape In String: Hello\\g"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_077():
    """Test illegal escape with h"""
    source = '"Hello\\hWorld"'
    expected = "Illegal Escape In String: Hello\\h"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_078():
    """Test illegal escape with i"""
    source = '"Hello\\iWorld"'
    expected = "Illegal Escape In String: Hello\\i"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_079():
    """Test illegal escape with j"""
    source = '"Hello\\jWorld"'
    expected = "Illegal Escape In String: Hello\\j"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_080():
    """Test illegal escape with k"""
    source = '"Hello\\kWorld"'
    expected = "Illegal Escape In String: Hello\\k"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_081():
    """Test illegal escape with l"""
    source = '"Hello\\lWorld"'
    expected = "Illegal Escape In String: Hello\\l"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_082():
    """Test illegal escape with m"""
    source = '"Hello\\mWorld"'
    expected = "Illegal Escape In String: Hello\\m"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_083():
    """Test illegal escape with o"""
    source = '"Hello\\oWorld"'
    expected = "Illegal Escape In String: Hello\\o"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_084():
    """Test illegal escape with p"""
    source = '"Hello\\pWorld"'
    expected = "Illegal Escape In String: Hello\\p"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_085():
    """Test illegal escape with q"""
    source = '"Hello\\qWorld"'
    expected = "Illegal Escape In String: Hello\\q"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_086():
    """Test illegal escape with s"""
    source = '"Hello\\sWorld"'
    expected = "Illegal Escape In String: Hello\\s"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_087():
    """Test illegal escape with u"""
    source = '"Hello\\uWorld"'
    expected = "Illegal Escape In String: Hello\\u"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_088():
    """Test illegal escape with v"""
    source = '"Hello\\vWorld"'
    expected = "Illegal Escape In String: Hello\\v"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_089():
    """Test illegal escape with w"""
    source = '"Hello\\wWorld"'
    expected = "Illegal Escape In String: Hello\\w"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_090():
    """Test illegal escape with z"""
    source = '"Hello\\zWorld"'
    expected = "Illegal Escape In String: Hello\\z"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_091():
    """Test complex expression tokens"""
    source = "let x = (a + b) * (c - d) / (e % f);"
    expected = "let,x,=,(,a,+,b,),*,(,c,-,d,),/,(,e,%,f,),;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_092():
    """Test function declaration tokens"""
    source = "func main() -> int { return 0; }"
    expected = "func,main,(,),->,int,{,return,0,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_093():
    """Test variable declaration tokens"""
    source = "let x: int = 42;"
    expected = "let,x,:,int,=,42,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_094():
    """Test const declaration tokens"""
    source = "const PI: float = 3.14159;"
    expected = "const,PI,:,float,=,3.14159,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_095():
    """Test if statement tokens"""
    source = "if (x > 0) { return x; } else { return -x; }"
    expected = "if,(,x,>,0,),{,return,x,;,},else,{,return,-,x,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_096():
    """Test while loop tokens"""
    source = "while (i < 10) { i = i + 1; }"
    expected = "while,(,i,<,10,),{,i,=,i,+,1,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_097():
    """Test for loop tokens"""
    source = "for (item in array) { print(item); }"
    expected = "for,(,item,in,array,),{,print,(,item,),;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_098():
    """Test array literal tokens"""
    source = "[1, 2, 3, 4, 5]"
    expected = "[,1,,,2,,,3,,,4,,,5,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_099():
    """Test function call tokens"""
    source = "calculate(a, b, c)"
    expected = "calculate,(,a,,,b,,,c,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_100():
    """Test complex nested expression tokens"""
    source = "let result = (a + b) >> (c * d) && (e == f);"
    expected = "let,result,=,(,a,+,b,),>>,(,c,*,d,),&&,(,e,==,f,),;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_101():
    """Test mixed literals and operators"""
    source = 'let message = "Hello" + " " + "World";'
    expected = "let,message,=,Hello,+, ,+,World,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_102():
    source = 'thisissomeid'
    expected = 'thisissomeid,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_103():
    source = 'fOOlzZZ'
    expected = 'fOOlzZZ,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_104():
    source = 'under__score'
    expected = 'under__score,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_105():
    source = 'the1andon1y'
    expected = 'the1andon1y,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_106():
    source = 'parser_RULE'
    expected = 'parser_RULE,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_107():
    source = 'vaRIAb1e567'
    expected = 'vaRIAb1e567,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_108():
    source = 'x__221'
    expected = 'x__221,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_109():
    source = 'mIxed13_andYoUxx__'
    expected = 'mIxed13_andYoUxx__,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_110():
    source = 'lOVrE_99_YOUr3000'
    expected = 'lOVrE_99_YOUr3000,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_111():
    source = 'aBBBBBx999rr0'
    expected = 'aBBBBBx999rr0,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_112():
    source = 'Aa'
    expected = 'Aa,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_113():
    source = 'aaaaa?bbbbb'
    expected = 'aaaaa,Error Token ?'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_114():
    source = 'withyou\n'
    expected = 'withyou,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_115():
    source = '1233what'
    expected = '1233,what,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_116():
    source = 'abcDEF'
    expected = 'abcDEF,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_117():
    source = 'a1b2c3'
    expected = 'a1b2c3,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_118():
    source = '___abc123'
    expected = '___abc123,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_119():
    source = 'A_B_C_123'
    expected = 'A_B_C_123,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_120():
    source = 'let x = 1; // comment'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_121():
    source = 'let y = 2; /* block comment */'
    expected = 'let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_122():
    source = 'let z = 3; /* nested /* block */ comment */'
    expected = 'let,z,=,3,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_123():
    source = 'if (a > b) { return a; } else { return b; }'
    expected = 'if,(,a,>,b,),{,return,a,;,},else,{,return,b,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_124():
    source = 'while (true) { break; }'
    expected = 'while,(,true,),{,break,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_125():
    source = 'for (i in arr) { continue; }'
    expected = 'for,(,i,in,arr,),{,continue,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_126():
    source = 'const PI = 3.14;'
    expected = 'const,PI,=,3.14,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_127():
    source = 'let s = "string with spaces";'
    expected = 'let,s,=,string with spaces,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_128():
    source = 'let arr = [1,2,3];'
    expected = 'let,arr,=,[,1,,,2,,,3,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_129():
    source = 'func add(a: int, b: int) -> int { return a + b; }'
    expected = 'func,add,(,a,:,int,,,b,:,int,),->,int,{,return,a,+,b,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_130():
    source = 'let flag = true && false || !true;'
    expected = 'let,flag,=,true,&&,false,||,!,true,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_131():
    source = 'let x = 1.23e-4;'
    expected = 'let,x,=,1.23e-4,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_132():
    source = 'let y = "Unclosed string'
    expected = 'let,y,=,Unclosed String: Unclosed string'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_133():
    source = 'let z = "Illegal \\q escape";'
    expected = 'let,z,=,Illegal Escape In String: Illegal \\q'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_134():
    source = 'let a = 0x123;'
    expected = 'let,a,=,0,x123,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_135():
    source = 'let b = 0o77;'
    expected = 'let,b,=,0,o77,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_136():
    source = 'let c = 007;'  # leading zeros
    expected = 'let,c,=,007,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_137():
    source = 'let d = -42;'
    expected = 'let,d,=,-,42,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_138():
    source = 'let e = 3.14e+10;'
    expected = 'let,e,=,3.14e+10,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_139():
    source = 'let f = "Hello\\nWorld";'
    expected = 'let,f,=,Hello\\nWorld,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_140():
    source = 'let g = "Hello\\tTab";'
    expected = 'let,g,=,Hello\\tTab,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_141():
    source = 'let h = "Hello\\rCarriage";'
    expected = 'let,h,=,Hello\\rCarriage,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_142():
    source = 'let i = "Hello\\Backslash";'
    expected = 'let,i,=,Illegal Escape In String: Hello\\B'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_143():
    source = 'let j = "He said \\"Hi\\"";'
    expected = 'let,j,=,He said \\"Hi\\",;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_144():
    source = 'let k = "";'
    expected = 'let,k,=,,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_145():
    source = 'let l = [true, false, true];'
    expected = 'let,l,=,[,true,,,false,,,true,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_146():
    source = 'let m = ["a", "b", "c"];'
    expected = 'let,m,=,[,a,,,b,,,c,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_147():
    source = 'let n = [1.1, 2.2, 3.3];'
    expected = 'let,n,=,[,1.1,,,2.2,,,3.3,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_148():
    source = 'let o = [1, [2, 3], 4];'
    expected = 'let,o,=,[,1,,,[,2,,,3,],,,4,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_149():
    source = 'let p = [[], []];'
    expected = 'let,p,=,[,[,],,,[,],],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_150():
    source = 'let q = [1, 2, 3, 4, 5];'
    expected = 'let,q,=,[,1,,,2,,,3,,,4,,,5,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_151():
    source = 'let r = ["hello", 42, true];'
    expected = 'let,r,=,[,hello,,,42,,,true,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_152():
    source = 'let s = [1, 2, [3, 4], 5];'
    expected = 'let,s,=,[,1,,,2,,,[,3,,,4,],,,5,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_153():
    source = 'let t = [1, 2, 3, [4, 5]];'
    expected = 'let,t,=,[,1,,,2,,,3,,,[,4,,,5,],],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_154():
    source = 'let u = [1, [2, [3, 4]], 5];'
    expected = 'let,u,=,[,1,,,[,2,,,[,3,,,4,],],,,5,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_155():
    source = 'let v = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];'
    expected = 'let,v,=,[,1,,,2,,,3,,,4,,,5,,,6,,,7,,,8,,,9,,,10,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_156():
    source = 'let w = [1];'
    expected = 'let,w,=,[,1,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_157():
    source = 'let x = [1, 2];'
    expected = 'let,x,=,[,1,,,2,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_158():
    source = 'let y = [1, 2, 3];'
    expected = 'let,y,=,[,1,,,2,,,3,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_159():
    source = 'let z = [1, 2, 3, 4];'
    expected = 'let,z,=,[,1,,,2,,,3,,,4,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_160():
    source = 'let arr = [1, 2, 3, 4, 5];'
    expected = 'let,arr,=,[,1,,,2,,,3,,,4,,,5,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_161():
    source = 'let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];'
    expected = 'let,arr,=,[,1,,,2,,,3,,,4,,,5,,,6,,,7,,,8,,,9,,,10,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_162():
    source = 'let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];'
    expected = 'let,arr,=,[,1,,,2,,,3,,,4,,,5,,,6,,,7,,,8,,,9,,,10,,,11,,,12,,,13,,,14,,,15,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_163():
    source = 'let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];'
    expected = 'let,arr,=,[,1,,,2,,,3,,,4,,,5,,,6,,,7,,,8,,,9,,,10,,,11,,,12,,,13,,,14,,,15,,,16,,,17,,,18,,,19,,,20,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_164():
    source = 'let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25];'
    expected = 'let,arr,=,[,1,,,2,,,3,,,4,,,5,,,6,,,7,,,8,,,9,,,10,,,11,,,12,,,13,,,14,,,15,,,16,,,17,,,18,,,19,,,20,,,21,,,22,,,23,,,24,,,25,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_165():
    source = 'let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30];'
    expected = 'let,arr,=,[,1,,,2,,,3,,,4,,,5,,,6,,,7,,,8,,,9,,,10,,,11,,,12,,,13,,,14,,,15,,,16,,,17,,,18,,,19,,,20,,,21,,,22,,,23,,,24,,,25,,,26,,,27,,,28,,,29,,,30,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_166():
    source = 'let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50];'
    expected = 'let,arr,=,[,1,,,2,,,3,,,4,,,5,,,6,,,7,,,8,,,9,,,10,,,11,,,12,,,13,,,14,,,15,,,16,,,17,,,18,,,19,,,20,,,21,,,22,,,23,,,24,,,25,,,26,,,27,,,28,,,29,,,30,,,31,,,32,,,33,,,34,,,35,,,36,,,37,,,38,,,39,,,40,,,41,,,42,,,43,,,44,,,45,,,46,,,47,,,48,,,49,,,50,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_167():
    source = "thisissomeid"
    expected = "thisissomeid,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_168():
    source = "fOOlzZZ"
    expected = "fOOlzZZ,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_169():
    source = "under__score"
    expected = "under__score,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_170():
    source = "the1andon1y"
    expected = "the1andon1y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_171():
    source = "parser_RULE"
    expected = "parser_RULE,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_172():
    source = "vaRIAb1e567"
    expected = "vaRIAb1e567,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_173():
    source = "x__221"
    expected = "x__221,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_174():
    source = "mIxed13_andYoUxx__"
    expected = "mIxed13_andYoUxx__,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_175():
    source = "lOVrE_99_YOUr3000"
    expected = "lOVrE_99_YOUr3000,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_176():
    source = "Aa"
    expected = "Aa,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_177():
    source = "aaaaa?bbbbb"
    expected = "aaaaa,Error Token ?"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_178():
    source = "withyou\n"
    expected = "withyou,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_179():
    source = "1233what"
    expected = "1233,what,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_180():
    source = "**just a glimpse of us**"
    expected = "*,*,just,a,glimpse,of,us,*,*,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_181():
    source = "Body Break Continue Do Else ElseIf EndBody EndIf"
    expected = "Body,Break,Continue,Do,Else,ElseIf,EndBody,EndIf,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_182():
    source = "EndFor EndWhile For Function If Parameter Return Then"
    expected = "EndFor,EndWhile,For,Function,If,Parameter,Return,Then,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_183():
    source = "Var While True False EndDo"
    expected = "Var,While,True,False,EndDo,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_184():
    source = "If if Else else"
    expected = "If,if,Else,else,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_185():
    source = "Do a whiLe b Return"
    expected = "Do,a,whiLe,b,Return,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_186():
    source = "DoNothing"
    expected = "DoNothing,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_187():
    source = "Do?While"
    expected = "Do,Error Token ?"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_188():
    source = "+-*\\==!=><>=<="
    expected = "+,-,*,Error Token \\"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_189():
    source = "+.-.*.\\.=/=<.>.<=.>=."
    expected = "+,.,-,.,*,.,Error Token \\"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_190():
    """Test string with newline characters (should be error)"""
    source = '"Hello\nWorld"'
    expected = "Unclosed String: Hello\n"
    assert Tokenizer(source).get_tokens_as_string() == expected


# Nested Block Comments Tests
def test_191():
    """Test simple nested block comment"""
    source = 'let x = 1; /* outer /* inner */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_192():
    """Test deeply nested block comments"""
    source = 'let x = 1; /* L1 /* L2 /* L3 */ L2 */ L1 */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_193():
    """Test nested comments with code inside"""
    source = 'let x = 1; /* outer /* let temp = 42; */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_194():
    """Test nested comments with strings inside"""
    source = 'let x = 1; /* outer /* "Hello World" */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_195():
    """Test nested comments with operators inside"""
    source = 'let x = 1; /* outer /* + - * / % */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_196():
    """Test nested comments with keywords inside"""
    source = 'let x = 1; /* outer /* func main if else while */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_197():
    """Test nested comments with numbers inside"""
    source = 'let x = 1; /* outer /* 123 3.14 true false */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_198():
    """Test nested comments with identifiers inside"""
    source = 'let x = 1; /* outer /* myVar _var123 */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_199():
    """Test nested comments with line comments inside"""
    source = 'let x = 1; /* outer /* // This is a line comment */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_200():
    """Test multiple nested comments on same line"""
    source = 'let x = 1; /* first /* inner1 */ */ let y = 2; /* second /* inner2 */ */ let z = 3;'
    expected = 'let,x,=,1,;,let,y,=,2,;,let,z,=,3,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_201():
    """Test nested comments with unmatched opening"""
    source = 'let x = 1; /* outer /* inner */'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_202():
    """Test nested comments with unmatched closing"""
    source = 'let x = 1; /* outer /* inner */ */ */ let y = 2;'
    expected = 'let,x,=,1,;,*,/,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_203():
    """Test nested comments with complex structure"""
    source = '''let x = 1; 
/* 
 * Outer comment 
 * /* Inner comment with code:
 *    let temp = 42;
 *    func helper() -> int { return 0; }
 * */ 
 * Back to outer comment 
 */ 
let y = 2;'''
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_204():
    """Test nested comments with special characters"""
    source = 'let x = 1; /* outer /* @#$%^&*()_+-=[]{}|\\:;"\'<>?,./ */ outer */ let y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_205():
    """Test nested comments with newlines"""
    source = '''let x = 1; 
/* outer 
   /* inner 
      with newlines 
   */ 
   outer continues */ 
let y = 2;'''
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

# Line Comments Tests
def test_206():
    """Test simple line comment"""
    source = 'let x = 1; // This is a comment'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_207():
    """Test line comment at start of line"""
    source = '// This is a comment at start\nlet x = 1;'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_208():
    """Test line comment with code after"""
    source = 'let x = 1; // comment\nlet y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_209():
    """Test multiple line comments"""
    source = '''// First comment
let x = 1;
// Second comment
let y = 2;
// Third comment'''
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_210():
    """Test line comment with special characters"""
    source = 'let x = 1; // @#$%^&*()_+-=[]{}|\\:;"\'<>?,./'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_211():
    """Test line comment with keywords inside"""
    source = 'let x = 1; // func main if else while for break continue'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_212():
    """Test line comment with operators inside"""
    source = 'let x = 1; // + - * / % == != < <= > >= && || !'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_213():
    """Test line comment with numbers inside"""
    source = 'let x = 1; // 123 3.14 1e10 true false'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_214():
    """Test line comment with identifiers inside"""
    source = 'let x = 1; // myVar _var123 func1 main2'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_215():
    """Test line comment with strings inside"""
    source = 'let x = 1; // "Hello World" "Test String"'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_216():
    """Test line comment with block comment markers inside"""
    source = 'let x = 1; // /* This is not a block comment */'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_217():
    """Test line comment with nested // inside"""
    source = 'let x = 1; // // This is still one line comment'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_218():
    """Test line comment with escape sequences inside"""
    source = 'let x = 1; // \\n\\t\\r\\\\\\"'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_219():
    """Test line comment with code-like content"""
    source = 'let x = 1; // let y = 2; func main() -> void { return 0; }'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_220():
    """Test line comment with array syntax inside"""
    source = 'let x = 1; // [1, 2, 3] arr[0] = 42;'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_221():
    """Test line comment with function call syntax inside"""
    source = 'let x = 1; // add(1, 2) print("hello")'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_222():
    """Test line comment with control flow syntax inside"""
    source = 'let x = 1; // if (x > 0) { return x; } else { return 0; }'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_223():
    """Test line comment with type annotations inside"""
    source = 'let x = 1; // let y: int = 42; func add(a: int, b: int) -> int'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_224():
    """Test line comment with pipeline operator inside"""
    source = 'let x = 1; // data >> process >> validate >> transform'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_225():
    """Test line comment with Unicode characters inside"""
    source = 'let x = 1; // 你好世界 Привет мир'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_226():
    """Test empty line comment"""
    source = 'let x = 1; //'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_227():
    """Test line comment with only spaces"""
    source = 'let x = 1; //    '
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_228():
    """Test line comment with tabs"""
    source = 'let x = 1; //\tThis comment has tabs'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_229():
    """Test line comment with carriage return"""
    source = 'let x = 1; // This comment ends with \r\nlet y = 2;'
    expected = 'let,x,=,1,;,let,y,=,2,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_230():
    """Test line comment with mixed content"""
    source = 'let x = 1; // Mixed: 123 "string" true false func() -> int'
    expected = 'let,x,=,1,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected 

def test_231():
    source = "1.0E123"
    expected = "1.0E123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_232():
    """Test valid string with escape characters"""
    source =  """12e52"""
    expected = '12,e52,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_233():
    """Test valid string with escape characters"""
    source =  """12e52"""
    expected = '12,e52,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_234():
    """Test scientific notation float literals"""
    source = "1.5e10 2.3E-5 1e+3 5E2"
    expected = "1.5e10,2.3E-5,1,e,+,3,5,E2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
    
def test_235():
    """Test arrow operator variations"""
    source = "-> --> -> ->"
    expected = "->,-,->,->,->,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_236():
    """Test pipeline operator variations"""
    source = ">> >>> >>>> >> >"
    expected = ">>,>>,>,>>,>>,>>,>,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_237():
    """Test not vs not equal"""
    source = "! != !== !=="
    expected = "!,!=,!=,=,!=,=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_238():
    source = "9a_z"
    expected = "9,a_z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_239():
    source = "Hello\nWorld"
    expected = "Hello,World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

