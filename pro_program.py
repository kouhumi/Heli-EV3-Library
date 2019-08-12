#!/usr/bin/env python3
from library import *
'''
Configurations for motors and sensors.
'''
def configure():
    a = motor('Large', 'A')

'''
Functions
'''
def forward():
    pass

def turn():
    pass

def swift():
    pass

def pid_forward():
    forward()

'''
Targeted Motions
'''
@timing
def target_1():
    # forward to death
    forward()

@timing
def target_2():
    # turn to death()
    turn()

def motions():
    target_1()
    target_2()


if __name__ == '__main__':
    configure()
    motions()