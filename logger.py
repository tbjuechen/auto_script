import logging

class ColoredFormatter(logging.Formatter):
    # 定义颜色
    COLORS = {
        'DEBUG': '\033[90m',   # Grey
        'INFO': '\033[94m',    # Blue
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[95m' # Magenta
    }
    RESET = '\033[0m'
    
    MSG_FORMAT = '%(asctime)s - %(module)s - %(message)s'

    # 确保标签长度一致
    FORMATS = {
        logging.DEBUG: COLORS['DEBUG'] + '[DEBUG]    ' + RESET + MSG_FORMAT,
        logging.INFO: COLORS['INFO'] + '[INFO]     ' + RESET + MSG_FORMAT,
        logging.WARNING: COLORS['WARNING'] + '[WARNING]  ' + RESET + MSG_FORMAT,
        logging.ERROR: COLORS['ERROR'] + '[ERROR]    ' + RESET + MSG_FORMAT,
        logging.CRITICAL: COLORS['CRITICAL'] + '[CRITICAL] ' + RESET + MSG_FORMAT
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        return formatter.format(record)

# 创建自定义 logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# 创建控制台处理器并设置级别为 DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建格式化器并将其添加到处理器
formatter = ColoredFormatter(datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)

# 将处理器添加到 logger
logger.addHandler(console_handler)

