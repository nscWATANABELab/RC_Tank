# (C) YanQ original
# (c) Noritomo Watanabe ver2
import RPi.GPIO as GPIO
import time

AIN1 = 10
AIN2 = 9
BIN1 = 25
BIN2 = 11

GPIO.setmode(GPIO.BCM)     # set mode
GPIO.setwarnings(False)    # do not show warning msg

GPIO.setup(AIN1, GPIO.OUT)  # motor's input AIN 1(right motor) 
GPIO.setup(AIN2, GPIO.OUT)  # motor's input AIN 2(right motor) 
GPIO.setup(BIN1, GPIO.OUT)  # motor's input BIN 1(left motor) 
GPIO.setup(BIN2, GPIO.OUT)  # motor's input BIN 2(letf motor)

# move_forward
def move_forward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.HIGH)
    # time.sleep(5)

# move_backward
def move_backward():
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
# turn_left
def turn_left():
    #GPIO.output(BIN1, GPIO.HIGH)
    #GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
# turn_right
def turn_right():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
# turn_right
# car stop
def stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    
# clean_GPIO
def clean_GPIO():
    GPIO.cleanup()



if __name__ == '__main__':
    # move_forward()
    clean_GPIO()