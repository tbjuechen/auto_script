from abc import ABC, abstractmethod


class BaseConnector(ABC):
    @abstractmethod
    def connect(self)->bool:
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def screen_shot(self, target_path:str):
        pass

    @abstractmethod
    def touch(self, position: tuple):
        pass

    @abstractmethod
    def drag(self, start: tuple, end: tuple, time:int):
        pass