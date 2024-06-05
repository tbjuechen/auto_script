from abc import ABC, abstractmethod
from typing import TypeVar, Generic

IMG = TypeVar('IMG')

class BasePlayer(ABC, Generic[IMG]):
    def __init__(self, acc:float=0.8, **kwargs) -> None:
        self.acc = acc  # 精度阈值


    @abstractmethod
    def locate(self, target:IMG, screenshot:IMG, debug:bool=False)->tuple:
        pass

    @abstractmethod
    def load_IMG(self, path:str)->IMG:
        pass

