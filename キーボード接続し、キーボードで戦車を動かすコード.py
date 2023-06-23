# http://ais.nsc.nagoya-cu.ac.jp/owncloud/index.php/apps/files/?dir=/%E5%90%8D%E5%B8%82%E5%A4%A7%E6%B8%A1%E9%82%8A%E7%A0%94%E7%A9%B6%E5%AE%A4%E5%85%B1%E6%9C%89%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80/data/tank&fileid=25559#editor よりコピー 
# 上記のプログラムを小林が説明のために中国語→日本語及び注釈を入れました2023.04.22(土)
# そのためこのプログラムで動かそうとすると、全角スペースなどの問題でエラーが出る可能性があります

# 收集数据，赛道照片和对应的前、后、左、右、4
# データを収集し、写真を追跡し、対応する前、後、左、右、4
# 外部機能をインポート(取り入れ)します
import io
import rc_control #rc_controlというモジュールをインポート 今回はいろんな所で使います
import os
os.environ['SDL_VIDEODRIVE'] = 'x11'
import pygame
from time import ctime,sleep,time # 時間に関する関数 41行目でsleep使う
import threading
import numpy as np #pythonの計算用モジュールnumpyをnpという名前で使いますという宣言
import picamera # picameraモジュールを使う宣言
import picamera.array # picameraモジュールの配列を使います宣言


global train_labels, train_img, is_capture_running, key # グローバル変数(このプログラムの中ならどこでも使える)の名前を宣言

# piカメラの動画キャプチャ関数の宣言部分
def pi_capture():
    global train_img, is_capture_running,train_labels,key
    
    #init the train_label 「array train_label」変数(配列)の初期化 initはinitiationの略で「初め」の意味
    print("Start capture")        
    is_capture_running = True # TrueかFalse(真か偽かのどちらか：Bool型のデータ)

    cameraT = picamera.PiCamera() #変数 cameraTにpicamera.PiCamera()のデータを入れます
    cameraT.start_preview(fullscreen=False, window=(50,50,1360,768))
    
    sleep(50)
    camera.stop_preview()
    
# RC_TANKのblue tooth キーボードの制御方法の記述
def my_car_control(): 
    global is_capture_running, key
    key = 4 # keyに4の数字を代入
    pygame.init()
    pygame.display.set_mode((1,1))            # 窗口 窓 display描写用のウィンドウやスクリーンを初期化
    rc_control.stop()
    sleep(0.1) # 0.1秒お休み
    print("Start control!")
 
    while is_capture_running: # キャプチャが働いている間のwhileブロック

        # get input from human driver 人がボタンを押して入力するのを待ち受け
        # 
        for event in pygame.event.get():
            # 判断事件是不是按键按下的事件 イベントがボタンを押下したかどうかを判別する
            if event.type == pygame.KEYDOWN:  
                key_input = pygame.key.get_pressed()     # 可以同时检测多个按键 複数のキーを同時に検出可能
                print(key_input[pygame.K_w], key_input[pygame.K_a], key_input[pygame.K_d])
                # 按下前进，保存图片以2开头 Wキー(進む)キーを押すと、画像は「2」から始まるファイルネームで保存されます
                if key_input[pygame.K_w] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                    print("Forward Down")
                    key = 2 
                    sleep(0.1)
                    rc_control.move_forward()
                # 按下左键，保存图片以0开头 Aキーを(左折)を押すと、画像は「0」から始まるファイルネームで保存されます
                elif key_input[pygame.K_a]:
                    print("Left Down")
                    rc_control.turn_left()
                    sleep(0.1)
                    key = 0
                # 按下d右键，保存图片以1开头 Dボタン(右折)を押すと、画像は「1」から始まるファイルネームで保存されます
                elif key_input[pygame.K_d]:
                    print("Right Down")
                    rc_control.turn_right()
                    sleep(0.1)
                    key = 1
                # 按下s后退键，保存图片为3开头 Sキー(戻る)を押すと、画像は「3」から始まるファイルネームで保存されます
                elif key_input[pygame.K_s]:
                    print("Backward Down")
                    rc_control.move_backward()
                    sleep(0.1)
                    key = 3
                # 按下k停止键，停止 停止するにはKキーを押します
                elif key_input[pygame.K_k]:
                    rc_control.stop()
            # 检测按键是不是抬起 キーが離されたかどうかを検出する
            elif event.type == pygame.KEYUP:
                key_input = pygame.key.get_pressed()
                # w键抬起，轮子回正 Wキーを離すと、ホイールが正しい位置に戻ります
                if key_input[pygame.K_w] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                    print("Forward Up")
                    key = 2
                    rc_control.stop()
                    rc_control.move_forward()
                # s键抬起 Sキーがアップした
                elif key_input[pygame.K_s] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                    print("Backward Up")
                    key = 3
                    rc_control.move_backward()
                else:
                    print("Stop")
                    rc_control.stop()
                #car_control.cleanGPIO()
    rc_control.clean_GPIO()

# プログラムはここから開始します
if __name__ == '__main__': #ここがプログラムがまる位置ですよという、pythonの書き方
    global train_labels, train_img, key

    print("capture thread") #プログラムが実際に始まったらコンソールに書きます
    print('-' * 50) # 次に50個の------でラインを書きます
    capture_thread = threading.Thread(target=pi_capture,args=())   # 开启线程 スレッドを開く
    capture_thread.setDaemon(True) #capture_thread.setDaemonはカメラキャプチャのプログラムを常駐(Daemon)させる(True)よと宣言
    capture_thread.start() #capture_threadをスタート
    
    my_car_control() #37行目のmy_car_controlを実行し、Start control!とコンソールに書きます

    while is_capture_running:
        pass

    print("Done!") # passを抜けたらDone!(おしまい)とコンソールに書いて
    rc_control.stop() #rc_controlをストップさせて
    cameraT.stop_preview() # cameraTをストップさせて
    rc_control.clean_GPIO() # rc_controlのclean_GPIOをしておしまい←clean_GPIOはrc_controlの値を全て0にする