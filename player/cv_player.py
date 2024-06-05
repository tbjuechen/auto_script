from .base_player import BasePlayer
from .timer import Timer

import cv2
from logging import getLogger, Logger
import numpy as np
from typing import Union, Callable
import time


class CVPlayer(BasePlayer[cv2.typing.MatLike]):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.logger:Logger = kwargs.get('logger', getLogger('logger'))

    def locate(
            self, 
            target:cv2.typing.MatLike, 
            screenshot:cv2.typing.MatLike, 
            debug:bool=False
            )->list[tuple[int,int]]:
        '''
        - 在截图中定位目标
        '''
        self.logger.debug('Locating from screenshot')
        positon: list[tuple[int,int]] = []  # 结果集合
        marks = []  # 标记集合 for debug

        target_h, target_w = target.shape[:2]  # shape: (height, width, channels)
        result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
        location = np.where(result >= self.acc)

        dis = lambda a, b: ((a[0]-b[0])**2 + (a[1]-b[1])**2) **0.5 #计算两点距离
        for y, x in zip(*location):
            center: tuple[int,int] = x + int(target_w/2), y + int(target_h/2)
            if positon and dis(positon[-1], center) < 20:  #忽略邻近重复的点
                continue
            else:
                positon.append(center)
                p2: tuple[int,int] = x + target_w, y + target_h
                marks.append(((x, y), p2))

        self.logger.info(f'Found {len(positon)} target(s)')
        if debug:
            self.logger.debug(f'Found {len(positon)} target(s)  ' + ' '.join([f'{i}: {mark}' for i, mark in enumerate(positon)]))
            for i, mark in enumerate(marks):
                screenshot = self.mark(screenshot, mark[0], mark[1])
            cv2.imshow(f'result for {111}:', screenshot)
            cv2.waitKey(0) 
            cv2.destroyAllWindows()

        return positon

    def load_IMG(self, path:str)->cv2.typing.MatLike:
        return cv2.imread(path)
    
    def mark(self, img:cv2.typing.MatLike, p1:tuple[int,int], p2:tuple[int,int])->None:
        '''
        - 在图像上标记矩形
        '''
        cv2.rectangle(img, p1, p2, (0, 0, 255), 2)
        return img
    
    def find(
            self, 
            target:Union[cv2.typing.MatLike,str], 
            screenshot:Union[cv2.typing.MatLike,str], 
            callback:Callable=None
            )->None:
        '''
        - 动作
        '''
        self.logger.debug('Finding target')
        
        # 加载图像
        if isinstance(target, str):
            target = self.load_IMG(target)
        if isinstance(screenshot, str):
            screenshot = self.load_IMG(screenshot)
        
        self.logger.debug('Image loaded')

        # 定位
        positions = self.locate(target, screenshot)
        if not positions:
            self.logger.warning('No target found')
            return
        self.logger.debug(f'touching at {str(positions[0])}')
        # 执行回调
        if callback:
            callback(positions[0])

    def _wait(self, seconds:int)->None:
        '''
        - 等待
        '''
        self.logger.debug(f'Waiting for {seconds} seconds')
        time.sleep(seconds)

    def wait_for(
            self,
            target:Union[cv2.typing.MatLike,str],
            shot:Callable,
            interval:int=0.5,
            timeout:int=10
            ):
        '''
        - 等待目标出现
        '''
        self.logger.debug('Waiting for target')
        if isinstance(target, str):
            target = self.load_IMG(target)
        
        positions = []
        with Timer(timeout) as timer:
            while timer.has_time_left():
                screenshot = self.load_IMG(shot())
                positions = self.locate(target, screenshot)
                if positions:
                    break
                self._wait(interval)
        return positions

