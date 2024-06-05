

class CannotConnectToHost(Exception):
    def __init__(self, *args: object, host:str, port:int) -> None:
        super().__init__(*args)
        self.host = host
        self.port = port

    def __str__(self) -> str:
        return f'Cannot connect to {self.host}:{self.port}'

class AlreadyConnected(Exception):
    def __init__(self, *args: object, host:str, port:int) -> None:
        super().__init__(*args)
        self.host = host
        self.port = port

    def __str__(self) -> str:
        return f'Already connected to {self.host}:{self.port}'
    
class NoSuchConnectError(Exception):
    def __init__(self, *args: object, host:str, port:int) -> None:
        super().__init__(*args)
        self.host = host
        self.port = port

    def __str__(self) -> str:
        return f'No such connect {self.host}:{self.port}'
    


class ShellError(Exception):
    def __init__(self, *args: object, host:str, port:int, msg:str) -> None:
        super().__init__(*args)
        self.host = host
        self.port = port
        self.msg = msg

    def __str__(self) -> str:
        return f'\'{self.msg}\' from {self.host}:{self.port}'
    
class ScreenShotError(ShellError):
    pass

class TouchError(ShellError):
    pass