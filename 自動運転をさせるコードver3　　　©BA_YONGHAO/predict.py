#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@ Author: Rindon
@ Date: 2025-01-06 16:20:25
@ LastEditors: Rindon
@ LastEditTime: 2025-01-16 14:18:11
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

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1280, 960)})
picam2.configure(config)

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
    img = cv2.imread(image_path)  # 生データ (BGR)
    img = img[:, :, ::-1].transpose(2, 0, 1).copy()  # BGR -> RGB, HWC -> CHW　yoloで処理できるサイズに変更する
    img = torch.from_numpy(img).to(device).float()  # tensorに変換する
    if img.ndimension() == 3:
        img = img.unsqueeze(0)  # batchの緯度を加える
    # 予測する
    pred = model(img)

    # 結果を解析する
    max_index = torch.argmax(pred,dim=1).item() #四種類の結果から最大値のIndexを取り出す
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
    print("ロード完了。")

    # 無限ループ
    try:
        while True:
            # 写真を撮る
            print("写真を撮ってる...")
            image_path = capture_image(TEMP_FOLDER)

            # 予測
            print("予測中...")
            class_name = predict_image(model, image_path, device)

            # 結果を返す
            print(f"予測結果: {class_name}")

            #移動する
            tank_Control(class_name)
                
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