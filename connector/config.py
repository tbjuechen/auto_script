import os

# 本地截图路径
SCREEN_SHOT_PATH_LOCAL:str = os.path.join(os.getcwd(), 'cache')
SCREEN_SHOT_NAME:str = 'screen_shot'

# 随机抖动
DEFAULT_OFFSET:tuple = (10, 10)