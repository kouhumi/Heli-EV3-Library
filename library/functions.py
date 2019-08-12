#!/usr/bin/env python3
from functools import wraps
import time
import threading

from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import *
from ev3dev2.sound import *

import library.config as config

'''
****************************************************
    'built-in' functions.
****************************************************
'''

delay = time.sleep
sgn = lambda x: 1 if x > 0 else(0 if x == 0 else -1)

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap


'''
****************************************************
    real-time sensor value.
****************************************************
'''

    
'''
****************************************************
    Declarations of motors and sensors.
****************************************************
'''

def motor(port):
    # validate motor port.
    try:
        port = config.motor_port_synonyms[port]
    except KeyError as e:
        print('port:', e, 'is not available. (Correct: A/B/C/D)')
        time.sleep(5)
        return None

    # try plugging in the motor as either of 2 types.
    try:
        m = LargeMotor(port)
    except Exception as e:
        try:
            m = MediumMotor(port)
        except Exception as e:
            print(port, 'is not connected. Check the motor, cable and the brick.')
            time.sleep(5)
            return None

    return m


def sensor(sensor_type, port = None): # plug in the default sensor port.
    # normalize sensor port.
    if port == 1 or port == '1':
        port = INPUT_1
    elif port == 2 or port == '2':
        port = INPUT_2
    elif port == 3 or port == '3':
        port = INPUT_3
    elif port == 4 or port == '4':
        port = INPUT_4
    elif port != None:
        print('Wrong sensor port. (Correct: 1/2/3/4)')
        delay(5)
        return None

    # normalize sensor type and plug it in.
    if sensor_type == 's' or sensor_type == 'S' or sensor_type == 'sonar' or sensor_type == 'Sonar' or sensor_type == 'ultrasonic' or sensor_type == 'Ultrasonic':
        if port == None:
            s = UltrasonicSensor()
        else:
            s = UltrasonicSensor(port)
        return s
    elif sensor_type == 't' or sensor_type == 'T' or sensor_type == 'touch' or sensor_type == 'Touch':
        if port == None:
            s = TouchSensor()
        else:
            s = TouchSensor(port)
        return s
    elif sensor_type == 'c' or sensor_type == 'C' or sensor_type == 'color' or sensor_type == 'Color':
        if port == None:
            s = ColorSensor()
        else:
            s = ColorSensor(port)
        return s
    else:
        print('Wrong sensor type. (Correct: \'sonar/\'touch)')
        delay(5)
        return None

def run(motor, speed, seconds = None): # run the motor forever.
    if seconds == None:
        status = 'unblocked'
    else:
        status = 'blocked'
    # if a single motor, list it.
    if isinstance(motor, (LargeMotor, MediumMotor)):
        motor = [motor]
    # if a single speed value, list it.
    if isinstance(speed, (int, float)):
        speed = [speed]
    # fill in the vacant speed.
    if len(speed) < len(motor):
        for i in range(len(motor) - len(speed)):
            speed.append(speed[-1])
    # eliminate speed outlier.
    for i in range(len(speed)):
        if speed[i] > 1050:
            speed[i] = 1050
        if speed[i] < -1050:
            speed[i] = -1050 

    # use .run_timed to run every motor.
    if seconds == None:
        for i in range(len(motor)):
            motor[i].run_forever(speed_sp = speed[i])
    else:
        for i in range(len(motor)):
            motor[i].run_forever(speed_sp = speed[i])
        time.sleep(seconds)
        for i in range(len(motor)):
            motor[i].stop()

def encoder_run(motor, speed, distance):
    pass

def pid_run(motor, distance, tolerance = 10):
    pass

def kalman_filtering():
    pass


def stop(motor):
    # if a single motor, list it.
    if isinstance(motor, (LargeMotor, MediumMotor)):
        motor.stop()
        return None
    elif isinstance(motor, list):
        for i in motor:
            if isinstance(i, (LargeMotor, MediumMotor)):
                i.stop()
    else:
        print('Wrong motor(s) to stop. \n(Correct: a = motor(\'Large\', 1)\n stop(a))')
        delay(5)
        return None

def get(sensor):
    if isinstance(sensor, (UltrasonicSensor, TouchSensor, ColorSensor)):
        if isinstance(sensor, (ColorSensor)):
            return colors[sensor.color]
        else:
            return sensor.value()
    else:
        print('Wrong sensor. \n(Correct: a = sensor(\'touch\')\n value(a))')
        delay(5)
        return None

def sonar_run(motor, speed, threshold = '>300', sonar = None):
# sonar_run(motor,speed) runs the motor until the default sonar sensor detects something close.
    # if a single motor, list it.
    if isinstance(motor, (LargeMotor, MediumMotor)):
        motor = [motor]
    # if a single speed value, list it.
    if isinstance(speed, (int, float)):
        speed = [speed]
    # fill in the vacant speed.
    if len(speed) < len(motor):
        for i in range(len(motor) - len(speed)):
            speed.append(speed[-1])
    # eliminate speed outlier.
    for i in range(len(speed)):
        if speed[i] > 1050:
            speed[i] = 1050
        if speed[i] < -1050:
            speed[i] = -1050 

    # use default sonar sensor.
    if sonar == None:
        sonar = UltrasonicSensor()

    # use .run_timed to run every motor.
    if threshold[0] == '>':
        while value(sonar) > int(float(threshold[1:])): 
            print(value(sonar))
            for i in range(len(motor)):
                motor[i].run_forever(speed_sp = speed[i])
        stop(motor)
    elif threshold[0] == '<':
        while value(sonar) < int(float(threshold[1:])):
            print(value(sonar))
            for i in range(len(motor)):
                motor[i].run_forever(speed_sp = speed[i])
        stop(motor)
    else:
        print('Wrong threshold. Correct(\'>300\'/\'<450\')')
        return None

def color_run(motor, speed, threshold, color = None):
    # if a single motor, list it.
    if isinstance(motor, (LargeMotor, MediumMotor)):
        motor = [motor]
    # if a single speed value, list it.
    if isinstance(speed, (int, float)):
        speed = [speed]
    # fill in the vacant speed.
    if len(speed) < len(motor):
        for i in range(len(motor) - len(speed)):
            speed.append(speed[-1])
    # eliminate speed outlier.
    for i in range(len(speed)):
        if speed[i] > 1050:
            speed[i] = 1050
        if speed[i] < -1050:
            speed[i] = -1050 
    
    # use default color sensor
    if color == None:
        color = ColorSensor()

    # use .run_forever to run every motor.
    if threshold[0] == '=' and threshold[1:] in colors:
        while value(color) == threshold[1:]: 
            print(value(color))
            for i in range(len(motor)):
                motor[i].run_forever(speed_sp = speed[i])
        stop(motor)
    elif threshold[0] == '!' and threshold[1] == '=' and threshold[2:] in colors: 
        while value(color) != threshold[2:]:
            print(value(color))
            for i in range(len(motor)):
                motor[i].run_forever(speed_sp = speed[i])
        stop(motor)
    else:
        print('Wrong threshold or colors. Correct(\'=black\'/\'!=blue\')\nColors: black, blue, green, yellow, red, white, brown')
        delay(5)
        return None

def waitfortouch(status = 'touch', touch = None):
# waitfortouch() waits until the default touch sensor is touched
    # normalize touch sensor
    if touch == None:
        touch = TouchSensor()
    elif not isinstance(touch, (TouchSensor)):
        print('Wrong touch sensor.\n(Correct: a = sensor(\'touch\')\n waitfortouch(a))')
        delay(5)
        return None

    # normalize statuses
    if status == 'touch' or status == 'Touch' or status == 'touched' or status == 'Touched':
        while value(touch) == 0:
            pass
        return None
    elif status == 'release' or status == 'Release' or status == 'released' or status == 'Released':
        while value(touch) == 1:
            pass
        return None
    elif status == 'click' or status == 'Click' or status == 'clicked' or status == 'Clicked':
        while value(touch) == 0:
            pass
        while value(touch) == 1:
            pass
        return None
    else:
        print('Wrong touch sensor status. (Correct: \'touch\'/\'release\')')
        delay(5)
        return None
        

if __name__ == '__main__':
    print('\n\n\nDo not run this program directly.')
    print('Create a .py file in the same path and import library.py.')
    while True:
        pass