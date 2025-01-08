#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@ Author: Rindon
@ Date: 2024-03-24 19:43:49
@ LastEditors: Rindon
@ LastEditTime: 2024-03-27 16:32:34
@ Description: Utils functions
'''

import pygame
import RPi.GPIO as GPIO
import threading
import numpy as np
import io
import os
os.environ['SDL_VIDEODRIVE'] = 'x11'
import time

# Global variable of GPIO port.
# DON'T change it except port changed.
AIN1 = 10 # 19
AIN2 = 9  # 21
BIN1 = 25 # 22
BIN2 = 11 # 23

key = 0

GPIO.setmode(GPIO.BCM)   
GPIO.setwarnings(False)   

GPIO.setup(AIN1, GPIO.OUT)  
GPIO.setup(AIN2, GPIO.OUT)   
GPIO.setup(BIN1, GPIO.OUT)  
GPIO.setup(BIN2, GPIO.OUT)  

'''
    @ description:'Functions about moving pi_Tank',
    @ param:'None',
    @ return:'None.'
'''
def move_forward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.HIGH)

def move_backward():
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)

def turn_left():
    GPIO.output(AIN1, GPIO.HIGH)

def turn_right():
    GPIO.output(BIN2, GPIO.HIGH)

def stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    
def clean_GPIO():
    GPIO.cleanup()

def test_Control():
    '''
        @ description:'Check the piTank by doing all the actions.',
        @ param:'None',
        @ return:'None.'
    '''
    move_forward()
    time.sleep(0.2)
    print('forward')
    stop()
    time.sleep(0.5)
    move_backward()
    time.sleep(0.2)
    print('backward')
    stop()
    time.sleep(0.5)
    turn_left()
    time.sleep(0.2)
    print('left')
    stop()
    time.sleep(0.5)
    turn_right()
    time.sleep(0.2)
    print('right')
    stop()

if __name__ == "__main__":
    test_Control()
