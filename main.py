from logger import logger
from connector.mumu_connector import MumuConnector
from player.cv_player import CVPlayer
import cv2

if __name__ == '__main__':


    # 测试
    connector = MumuConnector('127.0.0.1', 16384, name='testconnector')
    player = CVPlayer(acc=0.7)
    target_path = 'src/test/ok.jpg'
    screenshot_path = 'cache/screen_shot.jpg'
    connector.connect()
    connector.screen_shot()
    player.locate(player.load_IMG(target_path), player.load_IMG(screenshot_path), debug=True)
    # player.find(target_path, screenshot_path, callback=connector.touch)
    # while True:
    #     connector.touch(player.wait_for('src/test/yys_begin.jpg', connector.screen_shot, interval=1, timeout=10)[0])
    #     connector.touch(player.wait_for('src/test/yys_jieshu.jpg', connector.screen_shot, interval=1, timeout=10)[0])
    connector.disconnect()

   

    
    

