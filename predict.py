#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@ Author: Rindon
@ Date: 2025-01-06 16:20:25
@ LastEditors: Rindon
@ LastEditTime: 2025-01-06 16:33:40
@ Description: yoloを使って自動走行させる
'''

import os
import sys
import time
import torch
from picamera2 import Picamera2
from pathlib import Path,PosixPath
import cv2
from pi_Utils import *


# YOLOv5 ソースコードとモデルのパス
YOLOV5_PATH = "/home/pi/yolov5"  # YOLOv5ソースコードのパス
MODEL_PATH = "/home/pi/Desktop/m-last.pt" # モデルのパス

sys.path.append(YOLOV5_PATH)

#YOLOv5 のコアライブラリーを導入
from models.common import DetectMultiBackend
from utils.general import non_max_suppression
from utils.torch_utils import select_device

# 写真保存用フォルダーを作る
TEMP_FOLDER = "temp_images"

#torch cache folder
os.environ["TORCH_HOME"] = "/home/pi/.torch_cache"

picam2 = Picamera2()

def setup_temp_folder():
    """
    写真保存用フォルダーを作る、存在したら中をクリアする
    """
    if os.path.exists(TEMP_FOLDER):
        for file_name in os.listdir(TEMP_FOLDER):
            file_path = os.path.join(TEMP_FOLDER, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        os.makedirs(TEMP_FOLDER)

def capture_image(temp_folder, filename="image.jpg"):
    """

    Picamera2 を使って、写真を保存する
    :param temp_folder: フォルダーのパス
    :param filename: 写真ファイルの名前
    :return: 写真のパスを返す
    """
    # カメラのサイズとモードを配置する。６４０*６４０の方がおすすめ、原因は前と同じ。
    config = picam2.create_still_configuration(main={"size": (320, 240)})
    picam2.configure(config)
    picam2.start()

    time.sleep(1) #変なエラーを避けるため
    file_path = os.path.join(temp_folder, filename)
    picam2.capture_file(file_path)
    picam2.stop()

    return file_path

def predict_image(model, image_path, device):
    """
    YOLOv5 モデルを使って分類予測をする
    :param model: YOLOv5 モデル
    :param image_path: 写真ファイルのパス
    :param device: 予測用設備 (ここでCPU)
    :return max_index: 分類結果を返す（確率が一番高いもの）
    """
    # 写真を読み込む
    img0 = cv2.imread(image_path)  # 生データ (BGR)
    if img0 is None:
        print("img0 is None.Path error!")
    #print(img0.shape)
    # データの前処理
    img = cv2.resize(img0, (640,640))  # 写真サイズを調整する。もし直接６４０*６４０を利用する場合、この行が必要ない
    img = img[:, :, ::-1].transpose(2, 0, 1).copy()  # BGR -> RGB, HWC -> CHW　yoloで処理できるサイズに変更する
    img = torch.from_numpy(img).to(device).float()  # tensorに変換する
    img /= 255.0  # [0, 1]に均一化

    if img.ndimension() == 3:
        img = img.unsqueeze(0)  # batchの緯度を加える
    #print(img.shape)

    # 予測する
    pred = model(img)
    #print(pred)

    # 結果を解析する
    max_index = torch.argmax(pred,dim=1).item() #四種類の結果から最大値のIndexを取り出す
    #print(max_index)
    return max_index

def main():
    """
    アルゴリズムは以下になる：
    1. 写真保存用フォルダーを作る
    2. YOLOv5モデルをロードする
    3. 無限ループ：写真一枚撮る -> モデルを使って予測 -> 結果を返す
    """
    # 写真保存用フォルダーを作る
    setup_temp_folder()

    # YOLOv5モデルをロードする
    print("YOLOv5モデルをロード中...")
    device = select_device('cpu')  # 予測にはCPUで指定
    model = DetectMultiBackend(MODEL_PATH, device=device)
    if hasattr(model,"names"):
        model.names = [str(name) for name in model.names]
    model.names = model.names  # 分類タスクをとる
    print("ロード完了。")

    # 無限ループ
    try:
        while True:
            # 写真を撮る
            print("写真を撮ってる...")
            image_path = capture_image(TEMP_FOLDER)

            #print(image_path)
            # 予測
            print("予測中...")
            class_name = predict_image(model, image_path, device)

            # 結果を返す
            print(f"予測結果: {class_name}")

            #移動する
            if(class_name == 0):
                print("Turn left")
                turn_left()
                time.sleep(0.2)
                stop()
            elif(class_name == 1):
                print("Turn right")
                turn_right()
                time.sleep(0.2)
                stop()
            elif(class_name == 2):
                print("Move forward")
                move_forward()
                time.sleep(0.2)
                stop()
            else:
                print("Move backward")
                move_backward()
                time.sleep(0.2)
                stop()
                
    except KeyboardInterrupt:
        print("終わり。")
    finally:
        # フォルダーをクリアする
        for file_name in os.listdir(TEMP_FOLDER):
            file_path = os.path.join(TEMP_FOLDER, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        print("フォルダーをクリアした。")

if __name__ == "__main__":
    main()