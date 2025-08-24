# Kiến trúc Trình Biên Dịch
Dự án được tổ chức thành nhiều giai đoạn xử lý, tương ứng với từng Assignment trong môn học.

```
Source Code 
    ↓
Lexical Analysis (CSLexer) ← Assignment 1
    ↓  
Token Stream
    ↓
Syntax Analysis (CSParser) ← Assignment 1
    ↓
Parse Tree
    ↓
AST Generation (ASTGeneration) ← Assignment 2
    ↓
Abstract Syntax Tree (AST)
    ↓
Semantic Analysis (StaticChecker) ← Assignment 3
    ↓
Semantically Validated AST
    ↓
Code Generation (CodeGenerator) ← Assignment 4
    ↓
Jasmin Assembly Code (.j)
    ↓
JVM Bytecode (.class)
    ↓
Run Time & result
```

### 1. Source Code (.CS)
- Người dùng viết chương trình bằng ngôn ngữ **CS** trong file `.CS`.

---

### 2. Lexical Analysis (CSLexer) – Assignment 1
**Mục tiêu:** Phân tích từ vựng.  

- **Đầu vào:** Source code dạng chuỗi ký tự.  
- **Đầu ra:** Danh sách token (Token Stream).  

**Chức năng:**
- Nhận diện từ khóa, toán tử, ký hiệu, literal, identifier...
- Bỏ qua comment và whitespace.  
```c++
// erorr Lexer không đóng chuỗi
int main()
{
    std::string a = "votien

    return 0;
}
```

**Công cụ:** ANTLR để sinh lexer.

![](https://scaler.com/topics/images/lexical-analysis.webp)

---

### 3. Syntax Analysis (CSParser) – Assignment 1
**Mục tiêu:** Phân tích cú pháp.  

- **Đầu vào:** Token Stream từ Lexer.  
- **Đầu ra:** Parse Tree.  

**Chức năng:**
- Kiểm tra cấu trúc chương trình có tuân thủ grammar của CS không.  
- Xây dựng cây phân tích cú pháp (Parse Tree).  
```c++
// erorr Parser thiếu ;
int main()
{
    std::string a = "votien"

    return 0;
}
```

![](https://www.pling.org.uk/cs/lsaimg/parsetreetosyntaxtree.png)

---

### 4. AST Generation (ASTGeneration) – Assignment 2
**Mục tiêu:** Sinh **Abstract Syntax Tree (AST)** từ Parse Tree.  

- **Đầu vào:** Parse Tree.  
- **Đầu ra:** AST.  

**Chức năng:**
- Parse Tree chứa nhiều chi tiết dư thừa (ví dụ: dấu ngoặc, từ khóa).  
- AST giữ lại cấu trúc logic quan trọng để xử lý sau này.  

![](https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Flgfxjujkqwzz2iph2d4q.png)

---

### 5. Semantic Analysis (StaticChecker) – Assignment 3
**Mục tiêu:** Kiểm tra ngữ nghĩa tĩnh.  

- **Đầu vào:** AST.  
- **Đầu ra:** Semantically Validated AST (AST đã hợp lệ).  

**Chức năng:**
- Kiểm tra khai báo/định nghĩa biến, kiểu dữ liệu, phạm vi (scope).  
- Kiểm tra gọi hàm, gán, biểu thức logic...  
- Báo lỗi nếu vi phạm quy tắc ngữ nghĩa.  
```c++
// erorr StaticChecker return sai kiểu
int main()
{
    std::string a = "votien";

    return a;
}
```

---

### 6. Code Generation (CodeGenerator) – Assignment 4
**Mục tiêu:** Sinh mã đích (target code).  

- **Đầu vào:** AST đã hợp lệ.  
- **Đầu ra:** Jasmin Assembly `.j`.  

**Chức năng:**
- Chuyển AST sang Jasmin (ngôn ngữ assembly cho JVM).  
- Sinh các lệnh tương ứng cho biến, biểu thức, hàm, control flow.  

![](https://i.ytimg.com/vi/0G-31ZVjpTM/maxresdefault.jpg)

---

### 7. JVM Bytecode (.class)
- Jasmin Assembly `.j` được dịch sang JVM Bytecode `.class`.  
- Đây là mã máy ảo, có thể chạy trên bất kỳ JVM nào.  

---

### 8. Run Time & Result
- `.class` file được JVM chạy.  
- JVM thực thi bytecode và trả về kết quả chương trình.  