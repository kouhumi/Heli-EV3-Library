from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import *
from ev3dev2.sound import *

# synonyms for motor port.
motor_port_synonyms = {'a' : OUTPUT_A, 'A' : OUTPUT_A,
                       'b' : OUTPUT_B, 'B' : OUTPUT_B,
                       'c' : OUTPUT_C, 'C' : OUTPUT_C,
                       'd' : OUTPUT_D, 'D' : OUTPUT_D}

# synonyms for sensor port.
sensor_port_synonyms = {'1' : INPUT_1, 1 : INPUT_1,
                       '2' : INPUT_2, 2 : INPUT_2,
                       '3' : INPUT_3, 3 : INPUT_3,
                       '4' : INPUT_4, 4 : INPUT_4}
                

# values of the color sensor translated into colorful colors.
colors = ('No color', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

# threshold of speed values on a motor
speed_threshold = (-1050, 1050)