import io
import os
os.environ['SDL_VIDEODRIVE'] = 'x11'
import pygame
from time import ctime,sleep,time
import threading
import numpy as np
import picamera
import picamera.array
import RPi.GPIO as GPIO


AIN1 = 10 # 19
AIN2 = 9  # 21
BIN1 = 25 # 22
BIN2 = 11 # 23

GPIO.setmode(GPIO.BCM)     # set mode
GPIO.setwarnings(False)    # do not show warning msg

GPIO.setup(AIN1, GPIO.OUT)  # motor's input AIN 1(right motor) 
GPIO.setup(AIN2, GPIO.OUT)  # motor's input AIN 2(right motor) 
GPIO.setup(BIN1, GPIO.OUT)  # motor's input BIN 1(left motor) 
GPIO.setup(BIN2, GPIO.OUT)  # motor's input BIN 2(letf motor)

# move_forward
def move_forward():
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)

# move_backward
def move_backward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.HIGH)

# turn_left
def turn_left():
    GPIO.output(BIN1, GPIO.HIGH)

# turn_right
def turn_right():
    GPIO.output(AIN2, GPIO.HIGH)

# car stop
def stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    
# clean_GPIO
def clean_GPIO():
    GPIO.cleanup()

folder_path = '/home/pi/venv/DataCollection/right'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

folder_path1 = '/home/pi/venv/DataCollection/left'

if not os.path.exists(folder_path1):
    os.makedirs(folder_path1)

folder_path2 = '/home/pi/venv/DataCollection/forward'

if not os.path.exists(folder_path2):
    os.makedirs(folder_path2)

folder_path3 = '/home/pi/venv/DataCollection/back'

if not os.path.exists(folder_path3):
    os.makedirs(folder_path3)


global train_labels, train_img, is_capture_running, key

class SplitFrames(object):
    
    def __init__(self):
        self.frame_num = 0
        self.output = None
    def write(self, buf):
        global key
        if buf.startswith(b'\xff\xd8'):
            if self.output:
                self.output.close()
            self.frame_num += 1
            if key == 1:
                self.output = io.open('DataCollection/right/%s_image%s.jpg' % (key,time()), 'wb')
                
            elif key == 2:
                self.output = io.open('DataCollection/forward/%s_image%s.jpg' % (key,time()), 'wb')
                
            elif key == 3:
                self.output = io.open('DataCollection/back/%s_image%s.jpg' % (key,time()), 'wb')
            else:
                self.output = io.open('DataCollection/left/%s_image%s.jpg' % (key,time()), 'wb')
        self.output.write(buf)
    
 
def pi_capture():
    global train_img, is_capture_running,train_labels,key
    
    print("Start capture")        
    is_capture_running = True

    with picamera.PiCamera(resolution=(320, 240), framerate=30) as camera:
        sleep(2)
        output = SplitFrames()
        start = time()
        camera.start_recording(output, format='mjpeg')
        camera.wait_recording(120)
        camera.stop_recording()
        finish = time()
        print('Captured %d frames at %.2ffps' % (
        output.frame_num,
        output.frame_num / (finish - start)))
    
    print("quit pi capture")
    is_capture_running = False

def my_car_control(): 
    global is_capture_running, key
    key = 4
    pygame.init()
    pygame.display.set_mode((1,1))
    stop()
    sleep(0.1)
    print("Start control!")
 
    while is_capture_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  
                key_input = pygame.key.get_pressed()
                print(key_input[pygame.K_w], key_input[pygame.K_a], key_input[pygame.K_d])
                if key_input[pygame.K_w]: #and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                    print("Forward Down")
                    key = 2 
                    sleep(0.1)
                    move_forward()
                elif key_input[pygame.K_a]:
                    print("Left Down")
                    turn_left()
                    sleep(0.1)
                elif key_input[pygame.K_d]:
                    print("Right Down")
                    turn_right()
                    sleep(0.1)
                    key = 1
                elif key_input[pygame.K_s]:
                    print("Backward Down")
                    move_backward()
                    sleep(0.1)
                    key = 3
                elif key_input[pygame.K_k]:
                    stop()
            elif event.type == pygame.KEYUP:
                print("Stop")
                stop()
    rc_control.clean_GPIO()

if __name__ == '__main__':
    global train_labels, train_img, key

    print("capture thread")
    print('-' * 50)
    capture_thread = threading.Thread(target=pi_capture,args=())
    capture_thread.setDaemon(True)
    capture_thread.start()
    
    try:
        my_car_control()

        while is_capture_running:
            pass

        print("Done!")
    except KeyboardInterrupt:
        print("Finished")
    finally:
        stop()
        clean_GPIO()