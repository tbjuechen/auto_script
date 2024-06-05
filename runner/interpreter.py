from .base import BaseRunner, BaseVariable, BaseInterpreter
from .variable import Variable, Immediate
from .process_control import Main, Sequence, Branch, WhileLoop
from .function import Function

import json
from typing import Callable

BaseVariableDict:dict = {
    'int': {
        'type': int,
    },
    'float': {
        'type': float,
    },
    'str': {
        'type': str,
    },
    'bool': {
        'type': bool,
    },
    'pos': {
        'type': tuple,
        'from_str': lambda x: tuple(map(int, x[1:-1].split(','))),
    },
    }

BaseFuncDict:dict = {
    # 比较
    'eq': lambda x, y: x == y,
    'ne': lambda x, y: x != y,
    'lt': lambda x, y: x < y,
    'le': lambda x, y: x <= y,
    'gt': lambda x, y: x > y,
    'ge': lambda x, y: x >= y,
    # 逻辑
    'and': lambda x, y: x and y,
    'or': lambda x, y: x or y,
    'not': lambda x: not x,
    # 算术
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'mul': lambda x, y: x * y,
    'div': lambda x, y: x / y,
    'mod': lambda x, y: x % y,
    'pow': lambda x, y: x ** y,
    # io
    'print': print,
    }

class JSONInterpreter(BaseInterpreter):
    '''
    JSON解释器
    '''
    def __init__(self, variable_dict:dict = BaseVariableDict, func_dict:dict = BaseFuncDict):
        self.variable_dict = variable_dict
        self.func_dict = func_dict
        self.modules:dict = {
            'variable': self.handle_variable,
            'sequence': self.handle_sequence,
            'branch': self.handle_branch,
            'while': self.handle_while,
            'function': self.handle_function,
            'immediate': self.handle_immediate,
            }

    def handle(self, data:dict)->BaseRunner:
        if data is None:
            raise ValueError("Missing necessary components")
        if data['type'] in self.modules:
            return self.modules[data['type']](data)
        else:
            if data['type']:
                raise ValueError(f"Unknown type: {data['type']}")
            else:
                raise ValueError(f"Type is needed")

    def generate(self, data:dict) -> Main:
        '''
        生成Main
        '''
        self._temp_mian:Main = Main()
        
        def set_var(name:str, value):
            if self._temp_mian.exist_variable(name):
                self._temp_mian.get_variable(name).set(value)
            else:
                raise ValueError(f"Variable {name} not found")

        self.func_dict['set'] = set_var

        for item_src in data['steps']:
            item = self.handle(item_src)
            if isinstance(item, Variable):
                # 变量不加入步骤
                pass
            else:
                self._temp_mian.add_step(item)
        return self._temp_mian

    def handle_variable(self, data:dict)->Variable:
        '''
        转换为Variable  
        '''
        variable_type = data.get('variable_type')
        variable_name = data.get('name')
        if not variable_name:
            raise ValueError(f"Variable name is needed")
        elif variable_name in self._temp_mian.variables:
            # 变量已存在
            if self._temp_mian.variables[variable_name].type != variable_type:
                raise ValueError(f"Variable {variable_name} already exists with different type")
            else:
                return self._temp_mian.variables[variable_name]
            
        if not variable_type:
            raise ValueError(f"Variable type is needed")
        elif variable_type not in self.variable_dict:
            raise ValueError(f"Unknown variable type: {variable_type}")
        else:
            temp = Variable[self.variable_dict[variable_type]['type']](variable_name, variable_type)
            self._temp_mian.add_variable(temp)
            trans_func = self.variable_dict[variable_type].get('from_str')
            temp.set(data['value'], transform=trans_func)
            return temp
    
    def handle_sequence(self, data:dict)->Sequence:
        '''
        转换为Sequence
        '''
        steps:list[BaseRunner] = []
        for item_src in data['steps']:
            item = self.handle(item_src)
            if isinstance(item, Variable):
                # 变量不加入步骤
                pass
            else:
                steps.append(item)
        return Sequence(steps)
    
    def handle_branch(self, data:dict)->Branch:
        '''
        转换为Branch
        '''
        condition = self.handle(data['condition'])
        _then = self.handle(data['then'])
        _else = self.handle(data['else'])
        return Branch(condition, _then, _else)
    
    def handle_while(self, data:dict)->WhileLoop:
        '''
        转换为WhileLoop
        '''
        condition = self.handle(data['condition'])
        do = self.handle(data['do'])
        return WhileLoop(condition, do)
    
    def handle_function(self, data:dict)->Function:
        '''
        转换为Function
        '''
        target:Callable = self.func_dict[data['target']]
        args:list[BaseVariable] = [self.handle(arg) for arg in data['args']]
        return Function(target, args)
    
    def handle_immediate(self, data:dict)->Immediate:
        variable_type = data.get('variable_type')

        if not variable_type:
            raise ValueError(f"Variable type is needed")
        elif variable_type not in self.variable_dict:
            raise ValueError(f"Unknown variable type: {variable_type}")
        else:
            temp = Immediate[self.variable_dict[variable_type]['type']](variable_type)
            trans_func = self.variable_dict[variable_type].get('from_str')
            temp.set(data['value'], transform=trans_func)
            return temp