from logging import getLogger, Logger
import os
import random

from adb_shell.adb_device import AdbDeviceTcp

from .base_connector import BaseConnector
from ._exception import NoSuchConnectError, ScreenShotError, TouchError
from . import config



class Connector(AdbDeviceTcp, BaseConnector):
    '''
    - 连接器基类
    - 继承自AdbDeviceTcp
    - 实现了BaseConnector的接口
    '''
    def __init__(self, host:str, port:int, **kwargs):
        
        default_transport_timeout_s = kwargs.get('default_transport_timeout_s', None)
        banner = kwargs.get('banner', None)
        self.host = host
        self.port = port
        super().__init__(host, port, default_transport_timeout_s, banner)

        self.name = kwargs.get('name', None)
        self.logger:Logger = kwargs.get('logger', getLogger('logger'))
        self.logger.debug(f'Connector {self.name} created')

    def connect(self) -> bool:
        '''
        连接到设备
        '''
        self.logger.debug(f'Connecting to {self.host}:{self.port}')
        try:
            # 尝试连接
            super().connect()
            self.logger.info(f'Connected to {self.host}:{self.port}')
        except Exception as e:
            self.logger.error(type(e).__name__ + ': ' + str(e))

        return self._available

    def disconnect(self) -> bool:
        '''
        断开连接
        '''
        self.logger.debug(f'Disconnecting from {self.host}:{self.port}')
        try:
            if not self._available:
                raise NoSuchConnectError(host=self.host, port=self.port)
            # 尝试断开连接
            super().close() 
            self.logger.info(f'Disconnected from {self.host}:{self.port}')
        except Exception as e:
            self.logger.error(type(e).__name__ + ': ' + str(e))

        return self._available

    def shell(self, cmd:str) -> str:
        '''
        执行shell命令
        '''
        if not self._available:
            raise NoSuchConnectError(host=self.host, port=self.port)
        return super().shell(cmd)

    def screen_shot(self, target_path= config.SCREEN_SHOT_PATH_LOCAL, name:str=config.SCREEN_SHOT_NAME)-> str:
        '''
        截图
        '''
        if not os.path.exists(target_path):
            os.makedirs(os.path)
        try:
            # 截图
            cmd:str = f'screencap -p sdcard/Pictures/{name}.jpg'
            response = self.shell(cmd)
            if not response:
                self.logger.debug('Screenshot success')
            else:
                raise ScreenShotError(host=self.host, port=self.port,msg=response[:-1])
            # 下载
            target = os.path.join(target_path, name + '.jpg')
            self.pull(f'sdcard/Pictures/{name}.jpg', target)
            self.logger.info(f'Screenshot saved to {target}')
            return target
        except Exception as e:
            self.logger.error(type(e).__name__ + ': ' + str(e))
            exit(1)

    def random_offset(self, position: tuple[int,int], offset: tuple[int,int]=config.DEFAULT_OFFSET) -> tuple[int,int]:
        '''
        随机偏移
        '''
        x, y = position
        ox, oy = offset
        return x + random.randint(-ox, ox), y + random.randint(-oy, oy)

    def touch(self, position: tuple[int,int], offset:bool=True) -> bool:
        '''
        触摸
        '''
        try:
            self.logger.debug(f'Touch at {position}')
            if offset:
                position = self.random_offset(position)
            response = self.shell(f'input touchscreen tap {position[0]} {position[1]}')
            if not response:
                self.logger.debug('Touch success')
            else:
                raise TouchError(host=self.host, port=self.port,msg=response[:-1])
            return True
        except Exception as e:
            self.logger.error(type(e).__name__ + ': ' + str(e))
            return False

    def drag(self, start: tuple[int,int], end: tuple[int,int], time:int =1000, offset:bool=True) -> bool:
        '''
        滑动
        '''
        try:
            self.logger.debug(f'Drag from {start} to {end}')
            if offset:
                start = self.random_offset(start)
                end = self.random_offset(end)
            response = self.shell(f'input touchscreen swipe {start[0]} {start[1]} {end[0]} {end[1]} {time}')
            if not response:
                self.logger.debug('Drag success')
            else:
                raise TouchError(host=self.host, port=self.port,msg=response[:-1])
            return True
        except Exception as e:
            self.logger.error(type(e).__name__ + ': ' + str(e))
            return False
