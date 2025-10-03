"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))

        func_symbols = [
            Symbol(
                func.name,
                FunctionType([p.param_type for p in func.params], func.return_type),
                CName(self.class_name)
            )
            for func in node.func_decls
        ]
        
        global_env = reduce(lambda acc, ele: self.visit(ele, acc), node.const_decls + node.func_decls, SubBody(None, func_symbols + IO_SYMBOL_LIST))

        # Constructor
        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )

        # Const Declaration
        self.generate_method(
            FuncDecl("<clinit>", [], VoidType(), [
                Assignment(IdLValue(item.name), item.value) for item in node.const_decls
            ]),
            SubBody(Frame("<clinit>", VoidType()), global_env.sym)
        )

        # Write to runtime/HLang.j
        self.emit.emit_epilog()

    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame

        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        self.emit.print_out(
            self.emit.emit_method(
                node.name, FunctionType(param_types, return_type), not is_init
            )
        )

        frame.enter_scope(True)

        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # Generate code for parameters
        if is_init:
            this_idx = frame.get_new_index()

            self.emit.print_out(
                self.emit.emit_var(
                    this_idx, "this", ClassType(self.class_name), from_label, to_label
                )
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), from_label, to_label
                )
            )
        else:
            o = reduce(lambda acc, cur: self.visit(cur, acc), node.params, o)

        # start label
        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Generate code for body
        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        o = reduce(lambda acc, cur: self.visit(cur, acc), node.body, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
    
        # end label
        self.emit.print_out(self.emit.emit_label(to_label, frame))

        self.emit.print_out(self.emit.emit_end_method(frame))

        frame.exit_scope()

    def visit_const_decl(self, node: "ConstDecl", o: Any = None):
        frame = Frame(node.name, VoidType())

        if node.type_annotation is None:
            _, type_ = self.visit(node.value, Access(frame, o.sym))
        else: 
            type_ = node.type_annotation

        self.emit.print_out(
            self.emit.emit_attribute(
                node.name,
                type_,
                True,
                node.value
            )
        )

        return SubBody(
            None,
            [Symbol(node.name, type_, CName(self.class_name))] + o.sym
        )

    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        frame = Frame(node.name, node.return_type)
        self.generate_method(node, SubBody(frame, o.sym))
        param_types = list(map(lambda x: x.param_type, node.params))
        return SubBody(
            None,
            [
                Symbol(
                    node.name,
                    FunctionType(param_types, node.return_type),
                    CName(self.class_name),
                )
            ]
            + o.sym,
        )

    def visit_param(self, node: "Param", o: Any = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.param_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        return SubBody(
            o.frame,
            [Symbol(node.name, node.param_type, Index(idx))] + o.sym,
        )

    # Type system
    def visit_int_type(self, node: "IntType", o: Any = None):
        pass

    def visit_float_type(self, node: "FloatType", o: Any = None):
        pass

    def visit_bool_type(self, node: "BoolType", o: Any = None):
        pass

    def visit_string_type(self, node: "StringType", o: Any = None):
        pass

    def visit_void_type(self, node: "VoidType", o: Any = None):
        pass

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        pass

    # Statements

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        # Slot in local variable
        idx = o.frame.get_new_index()
        
        if node.type_annotation is None:
            _, type_ = self.visit(node.value, Access(o.frame, o.sym))
        else:
            type_ = node.type_annotation
        
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                type_,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        if node.value is not None:
            self.visit(
                Assignment(IdLValue(node.name), node.value),
                SubBody(
                    o.frame,
                    [Symbol(node.name, type_, Index(idx))] + o.sym,
                ),
            )
        
        return SubBody(
            o.frame,
            [Symbol(node.name, type_, Index(idx))] + o.sym,
        )

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        if type(node.lvalue) is ArrayAccessLValue:
            lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym))
            self.emit.print_out(lc)

            rc, rt = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(rc)
            if type(rt) is ArrayType and not type(node.value) is ArrayLiteral:
                self.emit.print_out(self.emit.emit_invoke_virtual(f"{self.emit.get_jvm_type(rt)}/clone()Ljava/lang/Object;", None, o.frame))
                self.emit.print_out(f"\tcheckcast {self.emit.get_jvm_type(rt)}\n")

            # iastore, fastore...
            self.emit.print_out(self.emit.emit_astore(lt, o.frame))
        else:
            # Load LHS
            rc, rt = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(rc)
            if type(rt) is ArrayType and not type(node.value) is ArrayLiteral:
                self.emit.print_out(self.emit.emit_invoke_virtual(f"{self.emit.get_jvm_type(rt)}/clone()Ljava/lang/Object;", None, o.frame))
                self.emit.print_out(f"\tcheckcast {self.emit.get_jvm_type(rt)}\n")

            lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym, True))
            self.emit.print_out(lc)
        return o

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        """
        condition: "Expr",
        then_stmt: "BlockStmt",
        elif_branches: List[tuple(condition, block)],
        else_stmt: Optional["BlockStmt"],
        """
        falseL = o.frame.get_new_label()
        endL = o.frame.get_new_label()
        ec,_ = self.visit(node.condition, Access(o.frame, o.sym))
        self.emit.print_out(ec)
        self.emit.print_out(self.emit.emit_if_false(falseL, o.frame))
        block = self.visit(node.then_stmt, o)

        self.emit.print_out(self.emit.emit_goto(endL, o.frame))
        if node.elif_branches:
            for cond, block in node.elif_branches:
                self.emit.print_out(self.emit.emit_label(falseL, o.frame))
                self.emit.print_out(self.visit(cond, Access(o.frame, o.sym))[0])
                falseL = o.frame.get_new_label()
                self.emit.print_out(self.emit.emit_if_false(falseL, o.frame))
                self.visit(block, o)
                self.emit.print_out(self.emit.emit_goto(endL, o.frame))
        self.emit.print_out(self.emit.emit_label(falseL, o.frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        self.emit.print_out(self.emit.emit_label(endL, o.frame))
        return o

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        """
        condition: "Expr"
        body: "BlockStmt"
        """
        o_temp = o
        o_temp.frame.enter_loop()
        # Create Labels
        continueL = o_temp.frame.get_continue_label()
        breakL = o_temp.frame.get_break_label()
        loopL = o_temp.frame.get_new_label()

        # While loop
        # loopL:
        self.emit.print_out(self.emit.emit_label(loopL, o_temp.frame))

        # Check condition in While
        self.emit.print_out(self.visit(node.condition, Access(o.frame, o_temp.sym))[0])
        self.emit.print_out(self.emit.emit_if_false(breakL, o_temp.frame))
        self.visit(node.body, o)

        # continueL:
        # goto loopL
        self.emit.print_out(self.emit.emit_label(continueL, o_temp.frame))
        self.emit.print_out(self.emit.emit_goto(loopL, o_temp.frame))

        # breakL:
        self.emit.print_out(self.emit.emit_label(breakL, o_temp.frame))
        o_temp.frame.exit_loop()
        return o

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        """
            variable: str 
            iterable: "Expr" 
            body: "BlockStmt"
        """
        o_temp = o
        o_temp = self.visit(VarDecl('for', IntType(), IntegerLiteral(0)), o_temp)
        o_temp = self.visit(VarDecl(node.variable, None, ArrayAccess(node.iterable, Identifier('for'))), o_temp)
        o_temp = self.visit(VarDecl('length', IntType(), FunctionCall(Identifier('len'), [node.iterable])), o_temp)
        o_temp.frame.enter_loop()
        # Create Labels
        continueL = o_temp.frame.get_continue_label()
        breakL = o_temp.frame.get_break_label()
        loopL = o_temp.frame.get_new_label()
        
        # For loop
        self.emit.print_out(self.emit.emit_label(loopL, o.frame))

        # Check condition: for < len -> BinaryOp(for, <, len) -> 1 / 0
        self.emit.print_out(self.visit(BinaryOp(Identifier('for'), '<', Identifier('length')), Access(o_temp.frame, o_temp.sym))[0])
        self.emit.print_out(self.emit.emit_ifeq(breakL, o_temp.frame))
        self.visit(Assignment(IdLValue(node.variable), ArrayAccess(node.iterable, Identifier('for'))), o_temp)
        self.visit(node.body, o_temp)
        
        # continueL:
        # goto loopL
        self.emit.print_out(self.emit.emit_label(continueL, o_temp.frame))
        # update for: for = for + 1
        o_temp = self.visit(
            Assignment(
                IdLValue('for'),
                BinaryOp(Identifier('for'), '+', IntegerLiteral(1))
            ), 
            o_temp
        )
        self.emit.print_out(self.emit.emit_goto(loopL, o_temp.frame))

        # breakL:
        self.emit.print_out(self.emit.emit_label(breakL, o_temp.frame))
        o_temp.frame.exit_loop()
        return o

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        if node.value:
            rc, rt = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(rc)
            self.emit.print_out(self.emit.emit_return(rt, o.frame))
        return

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        breakL = o.frame.get_break_label()
        self.emit.print_out(self.emit.emit_goto(breakL, o.frame))
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        continueL = o.frame.get_continue_label()
        self.emit.print_out(self.emit.emit_goto(continueL, o.frame))
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        """
        statements: List[Stmt]
        """
        o_temp = o
        o_temp = reduce(lambda acc, cur: self.visit(cur, acc), node.statements, o_temp)
        return o

    # Left-values
    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(
            filter(lambda x: x.name == node.name, o.sym),
            False,
        )

        value = sym.value
        if isinstance(value, Index):
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )
            type_ = sym.type
        else:
            # frame = Frame(sym.name, VoidType())
            type_ = sym.type

            code = self.emit.emit_put_static(
                self.class_name + "/" + sym.name, type_, o.frame
            )

        return code, type_

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Access = None):
        arrC,arrT = self.visit(node.array, o)
        indexC,_ = self.visit(node.index, o)
        code = arrC + indexC
        return code, arrT.element_type 
    
    # Expressions
    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        # Pipeline
        if node.operator in [">>"]:
            if isinstance(node.right, FunctionCall):
                function_call = FunctionCall(node.right.function, [node.left] + node.right.args)
            elif isinstance(node.right, Identifier):
                function_call = FunctionCall(node.right, [node.left])
            code, type_ = self.visit(function_call, o)
            return code, type_

        # Apply short-circuit
        if node.operator in ['||']:
            trueL = o.frame.get_new_label()
            endL = o.frame.get_new_label()
            code = self.visit(node.left, o)[0]
            code += self.emit.emit_if_true(trueL, o.frame)
            code += self.visit(node.right, o)[0]
            code += self.emit.emit_if_true(trueL, o.frame)
            code += self.emit.emit_push_iconst("0", o.frame)
            code += self.emit.emit_goto(endL, o.frame)
            code += self.emit.emit_label(trueL, o.frame)
            code += self.emit.emit_push_iconst("1", o.frame)
            code += self.emit.emit_label(endL, o.frame)
            return code, BoolType()
        if node.operator in ['&&']:
            endL = o.frame.get_new_label()
            falseL = o.frame.get_new_label()
            code = self.visit(node.left, o)[0]                  # iload_left
            code += self.emit.emit_if_false(falseL, o.frame)
            code += self.visit(node.right, o)[0]                # iload_right
            code += self.emit.emit_if_false(falseL, o.frame)
            code += self.emit.emit_push_iconst("1", o.frame)
            code += self.emit.emit_goto(endL, o.frame)
            code += self.emit.emit_label(falseL, o.frame)
            code += self.emit.emit_push_iconst("0", o.frame)
            code += self.emit.emit_label(endL, o.frame)
            return code, BoolType()

        codeLeft, typeLeft = self.visit(node.left, o)
        if node.operator in ['+'] and type(typeLeft) in [StringType]:
            _, typeRight = self.visit(node.right, Access(Frame("", ""), o.sym))

            if type(typeRight) is IntType:
                node.right = FunctionCall(Identifier("int2str"), [node.right])
            elif type(typeRight) is FloatType:
                node.right = FunctionCall(Identifier("float2str"), [node.right])
            elif type(typeRight) is BoolType:
                node.right = FunctionCall(Identifier("bool2str"), [node.right])
            codeRight, _ = self.visit(node.right, o)
            
            code = codeLeft + codeRight
            code += self.emit.emit_invoke_virtual("java/lang/String/concat", FunctionType([StringType()], StringType()), o.frame)
            return code, StringType()

        codeRight, typeRight = self.visit(node.right, o)
        if node.operator in ['+', '-'] and type(typeLeft) in [FloatType, IntType]:
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emit_i2f(o.frame)
                if type(typeRight) is IntType:
                    codeRight += self.emit.emit_i2f(o.frame)
            return codeLeft + codeRight + self.emit.emit_add_op(node.operator, typeReturn, o.frame), typeReturn
        elif node.operator in ['*', '/']:
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            """
            typeReturn:
                IntType: emit_div
                FloatType:
                    codeLeft/codeRight + i2f + emit_mul
            """
            if type(typeReturn) is IntType:
                if node.operator == "/":
                    return codeLeft + codeRight + self.emit.emit_div(o.frame), typeReturn
                return codeLeft + codeRight + self.emit.emit_mul_op(node.operator, typeReturn, o.frame), typeReturn

            # FloatType
            if type(typeLeft) is IntType:
                codeLeft += self.emit.emit_i2f(o.frame)
            if type(typeRight) is IntType:
                codeRight += self.emit.emit_i2f(o.frame)
            return codeLeft + codeRight + self.emit.emit_mul_op(node.operator, typeReturn, o.frame), typeReturn

        
        if node.operator in ['%']:
            return codeLeft + codeRight + self.emit.emit_mod(o.frame), IntType()
        if node.operator in ['==', '!=', '<', '>', '>=', '<='] and type(typeLeft) in [FloatType, IntType]:
            """
            int "op" int -> bool
            float "op" (int->float) -> bool
            (int->float) "op" float -> bool
            """
            if type(typeLeft) is IntType and type(typeRight) is IntType:
                return codeLeft + codeRight + self.emit.emit_re_op(node.operator, IntType(), o.frame), BoolType()

            if type(typeLeft) is IntType:
                codeLeft = codeLeft + self.emit.emit_i2f(o.frame)
            if type(typeRight) is IntType:
                codeRight = codeRight + self.emit.emit_i2f(o.frame)
            return codeLeft + codeRight + self.emit.emit_re_op(node.operator, FloatType(), o.frame), BoolType

        if node.operator in ['==', '!='] and type(typeLeft) in [BoolType]:
            code = codeLeft + codeRight
            code += self.emit.emit_re_op(node.operator, IntType(), o.frame)
            return code, BoolType()
        if node.operator in ['==', '!='] and type(typeLeft) in [StringType]:
            code = codeLeft + codeRight
            code += self.emit.emit_invoke_virtual("java/lang/String/compareTo", FunctionType([StringType()], IntType()), o.frame)
            code += self.emit.emit_push_iconst(0, o.frame)
            code += self.emit.emit_re_op(node.operator, IntType(), o.frame)
            return code, BoolType()   
            
    def visit_unary_op(self, node: "UnaryOp", o: Any = None):
        if node.operator == '!':
            code = self.visit(node.operand, o)[0]
            code += self.emit.emit_not(BoolType(), o.frame)
            return code, BoolType()
        code, type_return = self.visit(node.operand, o)
        return (code if node.operator == '+' else code + self.emit.emit_neg_op(type_return , o.frame)), type_return 

    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        function_name = node.function.name
        # if function_symbol is undefined
        if function_name == 'len':
            """
            Symbol:
                self.name = len
                self.type = FunctionType(ArrayType(), IntType())
                self.value = CName("io")
            """
            arrCode,_ = self.visit(node.args[0], o)
            arraylengthCode = "\t" + "arraylength" + "\n"
            return arrCode + arraylengthCode, IntType()
            
        function_symbol: Symbol = next(filter(lambda x: x.name == function_name, o.sym), False)

        argument_codes = []
        for argument in node.args:
            ac,at = self.visit(argument, Access(o.frame, o.sym))
            argument_codes += [ac]

        class_name = function_symbol.value.value
        return (
            "".join(argument_codes) 
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name, function_symbol.type, o.frame
            ),
            function_symbol.type.return_type
        )

    def visit_array_access(self, node: "ArrayAccess", o: Access = None) -> tuple[str, Type]:
        arrCode, arrType = self.visit(node.array, o)        # find array
        retType = arrType.element_type
        indexCode,_ = self.visit(node.index, o)             # take index
        codeGen = arrCode + indexCode + self.emit.emit_aload(retType, o.frame)
        return codeGen, retType
        
    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None) -> tuple[str, Type]:
        type_element_array = self.visit(node.elements[0], o)[1]
        codeGen = self.emit.emit_push_iconst(len(node.elements), o.frame)
        if o.frame.curr_op_stack_size > 2: 
            self.emit.emit_pop(o.frame)
        if  isinstance(type_element_array, (IntType, FloatType, BoolType)):
            codeGen += self.emit.emit_new_array(type_element_array)                 # newarray for primitive type
        else:
            codeGen += self.emit.emit_anew_array(type_element_array)                # anewarry
        for idx, item in enumerate(node.elements):
            codeGen += self.emit.emit_dup(o.frame)                                  # dup ref
            codeGen += self.emit.emit_push_iconst(idx, o.frame)                     # Index
            codeGen += self.visit(item, o)[0]                                       # Value
            codeGen += self.emit.emit_astore(type_element_array, o.frame)
        return codeGen, ArrayType(type_element_array, len(node.elements))  

    def visit_identifier(self, node: "Identifier", o: Access = None) -> tuple[str, Type]:
        """
        Identifier:
            name: str
        """
        sym = next(filter(lambda x: x.name == node.name, o.sym), False)
        """
        sym:
            name: str 
            _type: Type 
            value: Value
                Value: Index / CName
        """
        name = sym.name
        type_ = sym.type 
        value = sym.value           
        if isinstance(value, Index):
            """
            Index:
                value: int
            """
            if o.is_left is None:
                code = self.emit.emit_write_var(name, type_, value.value, o.frame)
            else:
                code = self.emit.emit_read_var(name, type_, value.value, o.frame)
        else:
            """
            CName:
                value: str
            """
            code = self.emit.emit_get_static(self.class_name + "/" + name, type_, o.frame)
        return code, type_

    # Literals
    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_fconst(node.value, o.frame), FloatType()

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Access = None) -> tuple[str, Type]:
        if node.value:
            return self.emit.emit_push_iconst(1, o.frame), BoolType()
        return self.emit.emit_push_iconst(0, o.frame), BoolType()

    def visit_string_literal(self, node: "StringLiteral", o: Access = None) -> tuple[str, Type]:
        return  self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame), StringType()
        
