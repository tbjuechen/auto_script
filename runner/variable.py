from .base import BaseRunner, BaseVariable
from typing import TypeVar, Generic, Union, get_args, Type, Callable

T = TypeVar('T')

class BaseData(BaseVariable, Generic[T]):
    def __init__(self, type:str):
        self.type = type
        self.value:T = None
        
    def get(self)->T:
        return self.value
    
    def set(self, value:T, transform:Callable=None)->None:
        self.value = transform(value) if transform else self._convert_to_type(value)

    def _convert_to_type(self, value: Union[T, Type[T]]) -> T:
        # 获取目标类型
        target_type = get_args(self.__orig_class__)[0]
        
        if isinstance(value, target_type):
            return value
        else:
            try:    
                return target_type(value)
            except Exception as e:
                raise ValueError(f"Cannot convert {value} to {target_type}: {e}")

    
class Variable(BaseData[T]):
    '''
    变量
    '''
    def __init__(self, name:str, type:str):
        super().__init__(type)
        self.name = name

class Immediate(BaseData[T]):
    '''
    立即数
    '''
    def __init__(self, type:str):
        super().__init__(type)