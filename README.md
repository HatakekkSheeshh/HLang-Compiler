# 🖥️ HLang-Compiler-Project

This repository contains a teaching compiler for the HLang/CS language used by the PPL-CS-HCMUT course. It implements the standard compiler pipeline:

- Lexical analysis (ANTLR lexer)
- Parsing (ANTLR parser)
- AST generation
- Static semantic checking
- Code generation to Jasmin assembly and JVM bytecode

This README explains how to set up the environment, build the ANTLR artifacts, run unit tests, and compile/run sample programs in `example/`.

## Quick overview

- Language: HLang (a small C/Python-like teaching language)
- Parser/lexer: ANTLR v4.13.2 (Python target)
- Runtime: Jasmin (assembly -> JVM bytecode)
- Tests: pytest

## Prerequisites

- Java (JRE/JDK) — used to run ANTLR and the JVM for running generated .class files
- Python 3.10+ and pip
- `antlr-4.13.2-complete.jar` (bundled in `external/`)
- Jasmin (`runtime/jasmin.jar`) is included for assembling .j -> .class

Recommended (Ubuntu/Debian):

```bash
# install system deps (example)
sudo apt update
sudo apt install -y openjdk-11-jdk python3 python3-pip
```

Install Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Build (generate parser/lexer)

ANTLR grammar files are in `src/grammar/`. The repository includes a helper script `build.sh` that calls the ANTLR jar and copies small helpers into `build/`.

Make the script executable and run it:

```bash
chmod +x build.sh
./build.sh
```

After running, generated Python parser/lexer files will be in the `build/` folder (the project already contains generated files for convenience).

## Running unit tests

The project uses `pytest`. Run the full test-suite:

```bash
pytest -q
```

You can run individual test modules, for example:

```bash
pytest tests/test_lexer.py -q
pytest tests/test_parser.py -q
pytest tests/test_ast_gen.py -q
pytest tests/test_checker.py -q
pytest tests/test_codegen.py -q
```

## Compile & run an example program

Example input programs are in the `example/` directory (e.g. `example/main.HLang`). The provided runner `run.py` performs a full pipeline: lex -> parse -> check -> codegen -> run (where applicable).

Basic usage:

```bash
python3 run.py example/main.HLang
# or
python3 run.py example/main
```

There are example files demonstrating errors:

- `example/error_lexer` — lexer error examples
- `example/error_parser` — parser error examples
- `example/error_checker` — semantic checker error examples

Use `run.py` with those files to see the error messages produced by each phase.

## Project layout

Top-level structure (high level):

- `build/` — generated ANTLR runtime artifacts (lexer/parser/visitor)
- `doc/` — documentation: setup and architecture notes
- `example/` — small example programs (good and error cases)
- `external/` — external binaries/jars (ANTLR jar)
- `runtime/` — Jasmin, helper Java code and prebuilt classes
- `src/` — compiler source code
  - `src/grammar/` — ANTLR grammar (`HLang.g4`)
  - `src/astgen/` — parse-tree -> AST conversion
  - `src/semantics/` — static checker and error classes
  - `src/codegen/` — code emission (Jasmin emitter, frame, codegen)
  - `src/utils/` — helpers (AST node types, visitor utilities, error listener)
- `tests/` — pytest unit tests
- `run.py` — convenience runner that exercises the full pipeline on an input file
- `build.sh` — helper script to run ANTLR and prepare `build/`
- `requirements.txt` — Python dependencies

## How the compiler pipeline works

1. Lexer: ANTLR-generated lexer tokenizes the source (handles special error tokens with `lexererr` helpers).
2. Parser: ANTLR-generated parser builds a parse tree.
3. AST Generation: `src/astgen/ast_generation.py` converts parse tree to AST nodes used by the rest of the compiler.
4. Semantic Analysis: `src/semantics/static_checker.py` performs scope/type checking and reports static errors.
5. Code Generation: `src/codegen/` emits Jasmin `.j` assembly and (via Jasmin) JVM `.class` bytecode. The `Emitter` and `Frame` classes are used to produce method/bytecode layout.

## Notable files

- `src/grammar/HLang.g4` — language grammar with lexer error handling
- `src/astgen/ast_generation.py` — AST generation visitor
- `src/semantics/static_checker.py` — static semantic checks and error classes
- `src/codegen/codegen.py` — code generator that emits Jasmin assembly
- `runtime/jasmin.jar` — included assembler to convert `.j` -> `.class`

## Troubleshooting

- If ANTLR fails to run, ensure the ANTLR jar is present at `external/antlr-4.13.2-complete.jar` and Java is installed.
- If imports fail after regenerating grammar files, ensure `build/` is on the Python import path or copy necessary generated files to a place Python can import.
- Use the provided `requirements.txt` to install the Python runtime dependencies.

## Contributing

1. Open an issue describing the bug/feature.
2. Create a branch, implement tests for bugs/features when possible, and submit a PR.

## License

See repository owner/instructor for license terms. This repo is a course project for instructional use.

---

If you'd like, I can also:

- add a short developer checklist for running the project in a devcontainer
- add explicit sample HLang programs in `example/` with expected output
- wire a simple Makefile to automate build/test/run

Tell me which of those you'd like next.