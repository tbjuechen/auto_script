from .base import BaseRunner, BaseVariable
from typing import Callable, Union


class Function(BaseRunner, BaseVariable):
    type = 'function'
    
    def __init__(self, target:Callable, args:list[BaseVariable]):
        self.target = target
        self.args = args

    def get(self):
        return self.run()

    def run(self):
        return self.target(*[arg.get() for arg in self.args])