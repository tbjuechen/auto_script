from .connector import Connector

class MumuConnector(Connector):
    def __init__(self, host: str='127.0.0.1', port: int=16384, **kwargs):
        super().__init__(host, port, **kwargs)