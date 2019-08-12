from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import *
from ev3dev2.sound import *

# synonyms for motor port.
motor_port_synonyms = {'a' : OUTPUT_A, 'A' : OUTPUT_A,
                       'b' : OUTPUT_B, 'B' : OUTPUT_B,
                       'c' : OUTPUT_C, 'C' : OUTPUT_C,
                       'd' : OUTPUT_D, 'D' : OUTPUT_D}

motor_type_synonyms = {'large'  : LargeMotor , 'Large'  : LargeMotor ,
                       'l'      : LargeMotor , 'L'      : LargeMotor ,
                       'medium' : MediumMotor, 'Meidum' : MediumMotor,
                       'm'      : MediumMotor, 'M'      : MediumMotor,
                       'middle' : MediumMotor, 'Middle' : MediumMotor}

# values of the color sensor translated into colorful colors.
colors = ('No color', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

# threshold of speed values on a motor
speed_threshold = (-1050, 1050)