# Do not try to run this code on a PC, this will not work.
import serial  # Interface with serial devices
import pywitmotion as wit  # Parses serial data from WT901 IMU
from pygame import mixer  # Play music using 'mixer' object
import math  # Math operations
import RPi.GPIO as GPIO  # Interface with GPIO Pins
import time

# Setup GPIO Inputs
GPIO.setmode(GPIO.BOARD)
buttonPin0 = 16
buttonPin1 = 18
buttonPin2 = 22
buttonPin3 = 24
GPIO.setup(buttonPin0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Store placeholders in velocity vector and angle list
velocity = [0, 0, 0]
angle = [0, 0, 0]

# Song tracks with corresponding file paths. Stored in 'songs' folder named 'track#'
track1 = 'songs/Melody1.wav'
track2 = 'songs/Chords1.wav'
track3 = 'songs/Drums1.wav'
track4 = 'songs/Bass1.wav'

# Setup pygame mixer and channels
mixer.init(channels=4)
mixer.Channel(0)
mixer.Channel(1)
mixer.Channel(2)
mixer.Channel(3)

# Serial baud rate to sample WitMotion data
baud = 9600

# Minimum velocity threshold to signal that IMU is in deliberate motion
# Change when needed, if IMU is too sensitive, increase this value and vice versa
threshold = 10


# Calculate magnitude of net velocity vector using distance equation d = sqrt(x^2 + y^2 + z^2)
def get_net_velocity(velocity_list):
    return math.sqrt((velocity_list[0] ** 2) + (velocity_list[1] ** 2) + velocity_list[2] ** 2)


with serial.Serial("/dev/ttyS0", baud, timeout=5) as ser:
    # Begin channels of music.
    # 'track#': corresponding track; 'loops=-1': loop indefinitely; 'fade_ms=1000': fade in and out 1sec
    mixer.Channel(0).play(mixer.Sound(file=track1), loops=-1)
    mixer.Channel(1).play(mixer.Sound(file=track2), loops=-1)
    mixer.Channel(2).play(mixer.Sound(file=track3), loops=-1)
    mixer.Channel(3).play(mixer.Sound(file=track4), loops=-1)

    while True:
        # Read byte of data from IMU until start bit(0x55 or U in ASCII)
        s = ser.read_until(b'U')

        # Get gyro and angle values while ignoring None-type values and storing in velocity and angle variable
        if wit.get_gyro(s) is not None:
            velocity = wit.get_gyro(s)

        if wit.get_angle(s) is not None:
            angle = wit.get_angle(s)

        # Check whether the IMU is moving.
        # Play music when velocity > threshold and pause when <= threshold
        if get_net_velocity(velocity) > threshold:
            mixer.Channel(0).unpause()
            mixer.Channel(1).unpause()
            mixer.Channel(2).unpause()
            mixer.Channel(3).unpause()

        elif get_net_velocity(velocity) <= threshold:
            mixer.Channel(0).pause()
            mixer.Channel(1).pause()
            mixer.Channel(2).pause()
            mixer.Channel(3).pause()

        # Signal for whether the reference angle has been set
        taredangle = False
        # Reads state of the button and runs program while the button is held down
        while GPIO.input(buttonPin0) == 0:
            # Reads serial data and stores velocity and angle
            mixer.Channel(0).unpause()
            mixer.Channel(1).unpause()
            mixer.Channel(2).unpause()
            mixer.Channel(3).unpause()
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                print("button0 pressed")
                angley_start = angle[1]
                taredangle = True

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if angle[1] - angley_start > 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(0).set_volume(mixer.Channel(0).get_volume() - 0.04)
                print("Volume0: " + str(mixer.Channel(0).get_volume()))
                print("Angle: " + str(angle[1]))

            if angle[1] - angley_start < 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(0).set_volume(mixer.Channel(0).get_volume() + 0.04)
                print("Volume: " + str(mixer.Channel(0).get_volume()))
                print("Angle: " + str(angle[1]))

        while GPIO.input(buttonPin1) == 0:
            # Reads serial data and stores velocity and angle
            mixer.Channel(0).unpause()
            mixer.Channel(1).unpause()
            mixer.Channel(2).unpause()
            mixer.Channel(3).unpause()
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                print("button1 pressed")
                angley_start = angle[1]
                taredangle = True

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if angle[1] - angley_start > 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(1).set_volume(mixer.Channel(1).get_volume() - 0.04)
                print("Volume1: " + str(mixer.Channel(1).get_volume()))
                print("Angle: " + str(angle[1]))

            if angle[1] - angley_start < 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(1).set_volume(mixer.Channel(1).get_volume() + 0.04)
                print("Volume: " + str(mixer.Channel(1).get_volume()))
                print("Angle: " + str(angle[1]))

        while GPIO.input(buttonPin2) == 0:
            # Reads serial data and stores velocity and angle
            mixer.Channel(0).unpause()
            mixer.Channel(1).unpause()
            mixer.Channel(2).unpause()
            mixer.Channel(3).unpause()
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                angley_start = angle[1]
                taredangle = True
                print("button2 pressed")

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if angle[1] - angley_start > 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(2).set_volume(mixer.Channel(2).get_volume() - 0.04)
                print("Volume1: " + str(mixer.Channel(2).get_volume()))
                print("Angle: " + str(angle[1]))

            if angle[1] - angley_start < 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(2).set_volume(mixer.Channel(2).get_volume() + 0.04)
                print("Volume: " + str(mixer.Channel(2).get_volume()))
                print("Angle: " + str(angle[1]))

        while GPIO.input(buttonPin3) == 0:
            # Reads serial data and stores velocity and angle
            mixer.Channel(0).unpause()
            mixer.Channel(1).unpause()
            mixer.Channel(2).unpause()
            mixer.Channel(3).unpause()
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                angley_start = angle[1]
                taredangle = True
                print("button3 pressed")

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if angle[1] - angley_start > 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(3).set_volume(mixer.Channel(3).get_volume() - 0.04)
                print("Volume1: " + str(mixer.Channel(3).get_volume()))
                print("Angle: " + str(angle[1]))

            if angle[1] - angley_start < 0 and abs(angle[1] - angley_start) > 10:
                mixer.Channel(3).set_volume(mixer.Channel(3).get_volume() + 0.04)
                print("Volume: " + str(mixer.Channel(3).get_volume()))
                print("Angle: " + str(angle[1]))
