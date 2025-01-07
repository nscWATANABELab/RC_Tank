#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@ Author: Rindon
@ Date: 2024-03-24 19:49:20
@ LastEditors: Rindon
@ LastEditTime: 2024-03-27 16:33:42
@ Description: Day 1 lesson: camera check
'''

import time
from picamera2 import Picamera2, Preview

def camera_Check():
    '''
        @ description:'Check camera status',
        @ param:'None',
        @ return:'None.'
    '''
    picam = Picamera2()

    config = picam.create_preview_configuration(main={"size": (320, 240)})
    picam.configure(config)

    picam.start_preview(Preview.QTGL)

    picam.start()
    time.sleep(10)

    picam.close()
    
if __name__ == "__main__":
	camera_Check()
	



