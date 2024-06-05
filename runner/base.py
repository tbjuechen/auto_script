from abc import ABC, abstractmethod


class BaseRunner(ABC):
    @abstractmethod
    def run(self):...

    def __call__(self):
        return self.run()
    

class BaseVariable(ABC):
    @abstractmethod
    def get(self):...

class BaseInterpreter(ABC):
    @abstractmethod
    def generate(data)->BaseRunner:...