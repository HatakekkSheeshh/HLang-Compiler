from typing import List, Optional
from .error import IllegalRuntimeException


class Frame:
    """
    Frame class to manage method frame information in code generation.
    
    Attributes:
        name (str): Name of the method
        curr_op_stack_size (int): Current size of operand stack
        max_op_stack_size (int): Maximum size of operand stack
        curr_index (int): Current index of local variable
        end_label (List[int]): Stack containing end labels of scopes
    """
    
    def __init__(self, name: str):
        self.name = name
        self.curr_op_stack_size = 0
        self.max_op_stack_size = 0
        self.curr_index = 0

    def push(self) -> None:
        self.curr_op_stack_size = self.curr_op_stack_size + 1
        if self.max_op_stack_size < self.curr_op_stack_size:
            self.max_op_stack_size = self.curr_op_stack_size

    def pop(self) -> None:
        self.curr_op_stack_size = self.curr_op_stack_size - 1
        if self.curr_op_stack_size < 0:
            raise IllegalRuntimeException("Pop empty stack")

    def get_max_op_stack_size(self) -> int:
        return self.max_op_stack_size

    def enter_scope(self) -> None:
        self.max_op_stack_size = 0
        self.curr_index = 0

    def exit_scope(self) -> None: pass

    def get_new_index(self) -> int:
        tmp = self.curr_index
        self.curr_index = self.curr_index + 1
        return tmp

    def get_max_index(self) -> int:
        return self.curr_index
