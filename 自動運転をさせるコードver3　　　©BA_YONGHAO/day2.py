#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@ Author: Rindon
@ Date: 2024-03-24 19:52:45
@ LastEditors: Rindon
@ LastEditTime: 2025-01-06 16:32:41
@ Description: Day 2 lesson: how to move pi_Tank
'''
from time import sleep
from pi_Utils import *

def keyboard_Control():
    '''
        @ description:'Move pi_Tank by using pygame',
        @ param:'key:{Forward : 2, Left : 0, Right : 1, Back : 3}',
        @ return:'None.'
    '''
    tank_Running = True
    global key
    key = 4
    pygame.init()
    pygame.display.set_mode((1,1)) #Actually shows nothing.
    stop()
    sleep(0.1)
    print("Start control!")
 
    while tank_Running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  
                key_input = pygame.key.get_pressed()
                #wprint(key_input[pygame.K_s], key_input[pygame.K_a], key_input[pygame.K_d])
                if key_input[pygame.K_w]:
                    key = 2
                elif key_input[pygame.K_a]:
                    key = 0
                elif key_input[pygame.K_d]:
                    key = 1
                elif key_input[pygame.K_s]:
                    key = 3
                elif key_input[pygame.K_k]:
                    stop()
            elif event.type == pygame.KEYUP:
                print("Stop")
                key = 4
                stop()
            if key is not None:
                key = tank_Control(key)
    tank_Running = False
    clean_GPIO()

if __name__ == "__main__":
    tank_Running = True
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
