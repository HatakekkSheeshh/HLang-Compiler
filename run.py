import sys
from tests.utils import Tokenizer, Parser, ASTGenerator, Checker, CodeGenerator

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py '<source_code>'")
        sys.exit(1)

    source_code = sys.argv[1]
    try:
        with open(source_code, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"[ERROR] File {source_code} not found")
        sys.exit(1)
        
    # Lexer
    tokenizer = Tokenizer(code)
    tokens = tokenizer.get_tokens_as_string()
    if "error" in tokens.lower():
        print("Lexer error:", tokens)
        sys.exit(1)

    # Parser
    parser = Parser(code)
    parse_result = parser.parse()
    if parse_result != "success":
        print("Parser error:", parse_result)
        sys.exit(1)

    # Static Checker
    checker = Checker(source=code)
    check_result = checker.check_from_source()
    if check_result != "Static checking passed":
        print("Static Checker error:", check_result)
        sys.exit(1)

    # Code Generator & Run
    codegen = CodeGenerator()
    output = codegen.generate_and_run(code)
    print("Program output:\n", output)

if __name__ == "__main__":
    main()
