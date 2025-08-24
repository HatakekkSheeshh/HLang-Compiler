import os
from typing import List, Optional, Union
from .jasmin_code import JasminCode
from .error import IllegalOperandException
from ..utils.nodes import *

class Emitter:
    def __init__(self, filename: str):
        self.filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "runtime", filename)
        self.buff: List[str] = []
        self.jvm = JasminCode()

    def get_jvm_type(self, in_type) -> str:
        type_in = type(in_type)
        if type_in is IntType:
            return "I"
        return in_type

    def emit_push_iconst(self, value, frame) -> str:
        frame.push()
        if value >= -1 and value <= 5:
            return self.jvm.emitICONST(value)
        elif value >= -128 and value <= 127:
            return self.jvm.emitBIPUSH(value)
        elif value >= -32768 and value <= 32767:
            return self.jvm.emitSIPUSH(value)
        else:
            return self.jvm.emitLDC(str(value))

    def emit_read_var(self, in_type, index: int, frame) -> str:
        frame.push()
        if type(in_type) is IntType :
            return self.jvm.emitILOAD(index)
        return self.jvm.emitALOAD(index)

    def emit_write_var(self, index: int, frame) -> str:
        frame.pop()
        return self.jvm.emitISTORE(index)
        
    def emit_invoke_special(self, frame) -> str:
        frame.pop()
        return self.jvm.emitINVOKESPECIAL()

    def emit_invoke_static(self, lexeme: str, in_, frame) -> str:
        frame.pop()
        return self.jvm.emitINVOKESTATIC(lexeme, self.get_jvm_type(in_))

    def emit_add_op(self, frame) -> str:
        frame.pop()
        return self.jvm.emitIADD()

    def emit_method(self, lexeme: str, in_type, is_static: bool) -> str:
        return self.jvm.emitMETHOD(lexeme, self.get_jvm_type(in_type), is_static)

    def emit_end_method(self, frame) -> str:
        buffer = list()
        buffer.append(self.jvm.emitLIMITSTACK(frame.get_max_op_stack_size()))
        buffer.append(self.jvm.emitLIMITLOCAL(frame.get_max_index()))
        buffer.append(self.jvm.emitENDMETHOD())
        return "".join(buffer)

    def emit_return(self) -> str:
        return self.jvm.emitRETURN()

    def emit_prolog(self, name: str, parent: str) -> str:
        result = list()
        result.append(self.jvm.emitSOURCE(name + ".java"))
        result.append(self.jvm.emitCLASS("public " + name))
        result.append(self.jvm.emitSUPER("java/land/Object" if parent == "" else parent))
        return "".join(result)

    def emit_epilog(self) -> None:
        file = open(self.filepath, "w")
        tmp = "".join(self.buff)
        file.write(tmp)
        file.close()

    def print_out(self, in_: str) -> None:
        self.buff.append(in_)

