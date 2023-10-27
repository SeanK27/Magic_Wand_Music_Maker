# Do not try to run this code on a PC, this will not work.
import serial  # Interface with serial devices
import pywitmotion as wit  # Parses serial data from WT901 IMU
from pygame import mixer  # Play music using 'mixer' object
import math  # Math operations
import RPi.GPIO as GPIO  # Interface with GPIO Pins
import time

# Setup GPIO Inputs
GPIO.setmode(GPIO.BCM)
buttonPin0 = 40
buttonPin1 = 1
buttonPin2 = 2
buttonPin3 = 3

# PUD_DOWN sets the internal pull down resistor
GPIO.setup(buttonPin0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonPin3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Store placeholders in velocity vector and angle list
velocity = [0, 0, 0]
angle = [0, 0, 0]

# Song tracks with corresponding file paths. Stored in 'songs' folder named 'track#'
track1 = 'songs/track1.mp3'
track2 = ''
track3 = ''
track4 = ''

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
threshold = 20


# Calculate magnitude of net velocity vector using distance equation d = sqrt(x^2 + y^2 + z^2)
def get_net_velocity(velocity_list):
    return math.sqrt((velocity_list[0] ** 2) + (velocity_list[1] ** 2) + velocity_list[2] ** 2)


with serial.Serial("/dev/ttyS0", baud, timeout=5) as ser:
    # Begin channels of music.
    # 'track#': corresponding track; 'loops=-1': loop indefinitely; 'fade_ms=1000': fade in and out 1sec
    mixer.Channel(0).play(mixer.Sound(file=track1), loops=-1, fade_ms=1000)
    mixer.Channel(2).play(mixer.Sound(file=track3), loops=-1, fade_ms=1000)
    mixer.Channel(3).play(mixer.Sound(file=track3), loops=-1, fade_ms=1000)
    mixer.Channel(4).play(mixer.Sound(file=track4), loops=-1, fade_ms=1000)

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
        elif get_net_velocity(velocity) <= threshold:
            mixer.Channel(0).pause()

        # Signal for whether the reference angle has been set
        taredangle = False
        # Reads state of the button and runs program while the button is held down
        while GPIO.input(buttonPin0) == GPIO.HIGH:
            # Reads serial data and stores velocity and angle
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                angley_start = angle[1]
                taredangle = True

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if abs(angley_start - angle[1]) > 5:
                # Set the volume to add or subtract off of the original volume based on the angle.
                # Full volume is 180degrees turned clockwise
                mixer.Channel(0).set_volume(mixer.Channel(0).get_volume() + (angle[1] - angley_start) / 180)
                # Reset the reference angle to prepare for next byte of data
                angley_start = angle[1]

        while GPIO.input(buttonPin1) == GPIO.HIGH:
            # Reads serial data and stores velocity and angle
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                angley_start = angle[1]
                taredangle = True

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if abs(angley_start - angle[1]) > 5:
                # Set the volume to add or subtract off of the original volume based on the angle.
                # Full volume is 180degrees turned clockwise
                mixer.Channel(1).set_volume(mixer.Channel(1).get_volume() + (angle[1] - angley_start) / 2)
                # Reset the reference angle to prepare for next byte of data
                angley_start = angle[1]

        while GPIO.input(buttonPin2) == GPIO.HIGH:
            # Reads serial data and stores velocity and angle
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                angley_start = angle[1]
                taredangle = True

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if abs(angley_start - angle[1]) > 5:
                # Set the volume to add or subtract off of the original volume based on the angle.
                # Full volume is 180degrees turned clockwise
                mixer.Channel(2).set_volume(mixer.Channel(2).get_volume() + (angle[1] - angley_start) / 2)
                # Reset the reference angle to prepare for next byte of data
                angley_start = angle[1]

        while GPIO.input(buttonPin3) == GPIO.HIGH:
            # Reads serial data and stores velocity and angle
            s = ser.read_until(b'U')
            if wit.get_angle(s) is not None:
                angle = wit.get_angle(s)

            # Sets reference angle of the IMU
            if not taredangle:
                angley_start = angle[1]
                taredangle = True

            # When the difference between the reference angle and the actual angle is greater than 5 (wand is rotated)
            if abs(angley_start - angle[1]) > 5:
                # Unpause Music when twist
                mixer.Channel(0).unpause()
                # Set the volume to add or subtract off of the original volume based on the angle.
                # Full volume is 180degrees turned clockwise
                mixer.Channel(3).set_volume(mixer.Channel(3).get_volume() + (angle[1] - angley_start) / 2)
                # Reset the reference angle to prepare for next byte of data
                angley_start = angle[1]
