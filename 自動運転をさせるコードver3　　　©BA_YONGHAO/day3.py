#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@ Author: Rindon
@ Date: 2024-03-24 20:22:52
@ LastEditors: Rindon
@ LastEditTime: 2025-01-16 14:18:49
@ Description: Day 3 lesson: collect data (Modified for Picamera2) 
'''
from pi_Utils import *
from day2 import *
import day2
from picamera2 import Picamera2
from time import time, sleep
import threading
import io
import os
import cv2


# データの保存場所を作る
folder_path = 'DataCollection/right/'
os.makedirs(folder_path, exist_ok=True)

folder_path1 = 'DataCollection/left/'
os.makedirs(folder_path1, exist_ok=True)

folder_path2 = 'DataCollection/forward/'
os.makedirs(folder_path2, exist_ok=True)

folder_path3 = 'DataCollection/back/'
os.makedirs(folder_path3, exist_ok=True)

# ビデオのフレームを保存するクラス
class SplitFrames:
    '''
        @ description: 'Class about IO',
        @ param: 'key,tank_Running',
        @ return: 'None.'
    '''
    global key, tank_Running

    def __init__(self):
        self.frame_num = 0  # フレームの数を記録

    def write(self, frame):
        self.frame_num += 1
        # 四種類のデータを別々で保存する
        if day2.key == 1:  # move right
            save_path = folder_path + f'{day2.key}_image{time()}.jpg'
        elif day2.key == 2:  # move forward
            save_path = folder_path2 + f'{day2.key}_image{time()}.jpg'
        elif day2.key == 3:  # move backward
            save_path = folder_path3 + f'{day2.key}_image{time()}.jpg'
        elif day2.key == 0:  # move left
            save_path = folder_path1 + f'{day2.key}_image{time()}.jpg'
        else:
            return

        # ファイルに保存する
        # 下のjpeg関数が使えないので、ここでOpenCVを使って写真を保存
        cv2.imwrite(save_path,frame)

# ラズパイのカメラを利用する関数
def pi_Capture():
    '''
    @ description: Function about pi_Camera for saving data (Modified for Picamera2).
    @ return: None
    '''
    print("Start capture.")
    global tank_Running
    tank_Running = True
    
    picam2 = Picamera2()

    # ビデオモードに変更
    video_config = picam2.create_video_configuration(main={"size": (1280, 960)}, buffer_count=4)
    picam2.configure(video_config)

    # カメラスタート
    picam2.start()
    sleep(2) 

    output = SplitFrames()
    start = time()
    duration = 120  # 撮る時間

    # ビデオのフレームを切って保存する
    try:
        while time() - start < duration:
            frame = picam2.capture_array()  # フレームデータを取る
            output.write(frame)  # フレームを保存
    except KeyboardInterrupt:
        print("キャプチャ中止")
    finally:
        picam2.stop()
        finish = time()
        print('Captured %d frames at %.2ffps' % (
            output.frame_num,
            output.frame_num / (finish - start)
        ))

    print("Quit pi capture.")
    tank_Running = False

if __name__ == "__main__":
    print("Capture thread")
    print('-' * 50)
    capture_thread = threading.Thread(target=pi_Capture, args=())
    capture_thread.setDaemon(True)
    capture_thread.start()

    try:
        keyboard_Control() 
        while tank_Running:
            pass
        print("Done!")
    except KeyboardInterrupt:
        print("Finished")
    finally:
        stop() 
        clean_GPIO() 