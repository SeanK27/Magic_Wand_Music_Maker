import serial  # Interface with serial devices
import pywitmotion as wit  # Parses serial data from WT901 IMU
import pygame  # Play music using 'mixer' object
import math  # Math operations

# Store placeholders in velocity vector and angle list
velocity = [0, 0, 0]
angle = [0, 0, 0]

# Song tracks with corresponding file paths. Stored in 'songs' folder named 'track#'
track1 = 'songs/track1.mp3'
track2 = ''
track3 = ''
track4 = ''

# Setup pygame mixer and channels
pygame.mixer.init(channels=4)
pygame.mixer.Channel(0)

# Serial baud rate to sample WitMotion data
baud = 115200

# Minimum velocity threshold to signal that IMU is in deliberate motion
# Change when needed, if IMU is too sensitive, increase this value and vice versa
threshold = 15


# Calculate magnitude of net velocity vector using distance equation d = sqrt(x^2 + y^2 + z^2)
def get_net_velocity(velocity_list):
    return math.sqrt((velocity_list[0] ** 2) + (velocity_list[1] ** 2) + velocity_list[2] ** 2)


with serial.Serial("COM6", baud, timeout=5) as ser:
    # Begin channels of music.
    # 'track#': corresponding track; 'loops=-1': loop indefinitely; 'fade_ms=1000': fade in and out 1sec
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(file=track1), loops=-1, fade_ms=1000)

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
            pygame.mixer.Channel(0).unpause()
        elif get_net_velocity(velocity) <= threshold:
            pygame.mixer.Channel(0).pause()
