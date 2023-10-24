import serial

def serial2hex(serial_data):

    hex_data = bytes.hex(serial_data)

    return hex_data

def convert_to_signed_short(high_byte, low_byte):

    signed_short = (high_byte << 8) | low_byte

    return signed_short

def get_acceleration_data(serial_port):

    # Read 11 bytes of data from the serial port.
    hex_data = serial_port.readline(11)

    # Extract the acceleration data from the hexadecimal data.
    x_acceleration = convert_to_signed_short(hex_data[2], hex_data[3])
    y_acceleration = convert_to_signed_short(hex_data[4], hex_data[5])
    z_acceleration = convert_to_signed_short(hex_data[6], hex_data[7])

    return x_acceleration, y_acceleration, z_acceleration


# Open the serial port to the IMU sensor.
serial_port = serial.Serial('COM6', 9600)

# Get the acceleration data from the IMU sensor.

while True:
    x_acceleration, y_acceleration, z_acceleration = get_acceleration_data(serial_port)

    # Print the acceleration data.
    print('X acceleration:', x_acceleration)
    print('Y acceleration:', y_acceleration)
    print('Z acceleration:', z_acceleration)

    # Close the serial port.


serial_port.close()