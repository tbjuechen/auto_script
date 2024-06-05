from .base import BaseRunner, BaseVariable
from .variable import Variable

from typing import Callable, Union

class Sequence(BaseRunner):
    '''
    顺序执行
    '''
    type = 'sequence'
    
    def __init__(self, steps:list[BaseRunner]):
        self.steps = steps

    def run(self):
        for step in self.steps:
            step.run()

class Branch(BaseRunner):
    '''
    分支
    '''
    type = 'branch'

    def __init__(self, condition:BaseVariable, _then:BaseRunner, _else:BaseRunner):
        self.condition = condition
        self._then = _then
        self._else = _else
    
    def run(self):
        if self.condition.get():
            self._then()
        else:
            self._else()

class WhileLoop(BaseRunner):
    '''
    循环
    '''
    type = 'while'

    def __init__(self, condition:BaseVariable, do:BaseRunner):
        self.condition = condition
        self.do = do

    def run(self):
        while self.condition.get():
            self.do()

class Main(Sequence):
    '''
    主函数
    '''
    type = 'main'

    def __init__(self, steps:list[BaseRunner]=None):
        if steps is None:
            steps = []
        super().__init__(steps)
        self.variables:dict[str,Variable] = {}

    def exist_variable(self, name:str)->bool:
        '''
        - 是否存在变量
        '''
        return name in self.variables
    
    def get_variable(self, name:str)->Variable:
        '''
        - 获取变量
        '''
        if self.exist_variable(name):
            return self.variables[name]
        else:
            raise ValueError(f"Variable {name} not found")
    
    def add_variable(self, variable:Variable):
        '''
        - 添加变量
        '''
        name = variable.name
        if self.exist_variable(name):
            raise ValueError(f"Variable {name} already exists")
        else:
            self.variables[name] = variable

    
    def add_step(self, step:BaseRunner):
        '''
        - 添加步骤
        '''
        self.steps.append(step)
    
    