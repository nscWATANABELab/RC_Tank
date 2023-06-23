# (C) YanQ original
# (c) Noritomo Watanabe ver2
import os
import io
import glob
import time
import threading
import picamera.array
import picamera
from PIL import Image
import numpy as np

import rc_control_wata
from tensorflow.keras.models import load_model
import tensorflow.compat.v1 as tf
from tensorflow.keras.backend import clear_session


def get_max_prob_num(predictions_array):
    prediction_edit = np.zeros([1, 4])
    for i in range(0, 4):
        if predictions_array[0][i] == predictions_array.max():
            prediction_edit[0][i] = 1
            return i
    return 2


def control_car(action_num):
    if action_num == 1:
        print("Left")
        rc_control_wata.turn_left()
        time.sleep(0.1)
        rc_control_wata.stop()
    elif action_num == 0:
        print("Right")
        rc_control_wata.turn_right()
        time.sleep(0.1)
        rc_control_wata.stop()
    elif action_num == 2:
        print("Forward")
        rc_control_wata.move_forward()
        time.sleep(0.5)
        rc_control_wata.stop()
    elif action_num == 3:
        rc_control_wata.move_backward()
        time.sleep(0.5)
        rc_control_wata.stop()
        print("Backward")
    else:
        rc_control_wata.stop()
        print('stop')


class ImageProcessor(threading.Thread):
    def __init__(self, owner):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.owner = owner
        self.start()
    def run(self):
        global latest_time, model, graph
        while not self.terminated:
            if self.event.wait():
                try:
                    self.stream.seek(0)
                    image = Image.open(self.stream)
                    image_np = np.array(image)
                    camera_data_array = np.expand_dims(image_np, axis=0).astype(np.float32)
                    current_time = time.time()
                    if current_time > latest_time:
                        latest_time = current_time
                        prediction_array = model.predict(camera_data_array)
                        action_num = get_max_prob_num(prediction_array)
                        control_car(action_num)
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    with self.owner.lock:
                        self.owner.pool.append(self)

class ProcessOutput(object):
    def __init__(self):
        self.done = False
        self.lock = threading.Lock()
        self.pool = [ImageProcessor(self) for i in range(4)]
        self.processor = None
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            if self.processor:
                self.processor.event.set()
            with self.lock:
                if self.pool:
                    self.processor = self.pool.pop()
                else:
                    self.processor = None
        if self.processor:
            self.processor.stream.write(buf)

    def flush(self):
        if self.processor:
            with self.lock:
                self.pool.append(self.processor)
                self.processor = None
        while True:
            with self.lock:
                try:
                    proc = self.pool.pop()
                except IndexError:
                    pass
            proc.terminated = True
            proc.join()




def main():
    clear_session()
    global model, graph
    model = load_model("model-006.h5")
    model._make_predict_function()    
    try:
        # """
        with picamera.PiCamera(resolution=(160, 120)) as camera:
            time.sleep(2)
            output = ProcessOutput()
            camera.start_recording(output, format='mjpeg')
            while not output.done:
                camera.wait_recording(1)
            camera.stop_recording()
        # """
    except KeyboardInterrupt:
        print("ki")
    finally:
        rc_control.clean_GPIO()
    print("finished")

if __name__ == '__main__':
    global latest_time
    latest_time = time.time()
    main()