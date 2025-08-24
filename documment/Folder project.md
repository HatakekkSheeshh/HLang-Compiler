## Cấu trúc thư mục project

```
workspace/

├── README.md           # Tài liệu giới thiệu project
|
├── .devcontainer/
│ ├── Dockerfile        # Định nghĩa môi trường phát triển (Dev Container)
│ ├── banner.sh         # Script hiển thị banner khi container khởi động
│ └── devcontainer.json # Cấu hình Dev Container (VS Code)
|
├── build/              # Thư mục chứa file sinh tự động từ ANTLR
│
├── build.sh            # Script build lexer/parser từ ANTLR
│
├── documment/          # Thư mục tài liệu
│
├── example/            # Ví dụ chương trình viết bằng HLang
│ ├── error_checker     # Ví dụ gây lỗi ngữ nghĩa
│ ├── error_lexer       # Ví dụ gây lỗi từ vựng
│ ├── error_parser      # Ví dụ gây lỗi cú pháp
│ └── main              # Ví dụ chương trình chạy thành công
│
├── external/
│ └── antlr-4.13.2-complete.jar # ANTLR tool để build Lexer/Parser
│
├── run.py # File Python chạy toàn bộ pipeline (lexer → parser → checker → codegen → run)
│
├── src/
│ ├── astgen/              # BTL2 Module sinh AST từ Parse Tree
│ │ └── ast_generation.py
│ │
│ ├── codegen/             # BTL4 Module sinh mã Jasmin từ AST
│ │ ├── codegen.py           # Trình sinh code chính
│ │ ├── emitter.py           # Quản lý sinh mã
│ │ ├── frame.py             # Quản lý frame / stack JVM
│ │ ├── jasmin_code.py       # Sinh code Jasmin
│ │ └── error.py             # Định nghĩa Lỗi sinh code
│ │
│ ├── grammar/             # BTL1 Định nghĩa ngữ pháp ANTLR
│ │ ├── CS.g4                # File grammar chính
│ │ └── lexererr.py          # Định nghĩa Lỗi lexer
│ │
│ ├── runtime/             # BTL4 Thư mục runtime (chạy chương trình biên dịch ra)
│ │ ├── CS.class             # Bytecode sau khi assemble
│ │ ├── CS.j                 # File Jasmin sinh ra
│ │ ├── io.java              # File IO hỗ trợ chạy chương trình
│ │ ├── io.class             # Bytecode của io.java
│ │ └── jasmin.jar           # Jasmin assembler
│ │
│ ├── semantics/           # BTL3 Module kiểm tra ngữ nghĩa
│ │ ├── static_checker.py    # StaticChecker chính
│ │ └── static_error.py      # Định nghĩa lỗi ngữ nghĩa
│ │
│ └── utils/               # Module tiện ích
│ ├── error_listener.py       # Custom error listener cho ANTLR
│ ├── nodes.py                # Định nghĩa node AST
│ └── visitor.py              # Visitor pattern cho AST
│
├── tests/                 # Bộ kiểm thử với pytest
│ ├── test_lexer.py           # BTL1 Test Lexer
│ ├── test_parser.py          # BTL1 Test Parser
│ ├── test_ast_gen.py         # BTL2 Test AST Generation
│ ├── test_checker.py         # BTL3 Test Semantic Checker
│ ├── test_codegen.py         # BTL4 Test Code Generator
│ └── utils.py                # Tiện ích dùng cho test
│
└── build.sh # Script build grammar
```