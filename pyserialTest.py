import serial

def serial2hex(serial_data):

    hex_data = bytes.hex(serial_data)

    return hex_data

def convert_to_signed_short(high_byte, low_byte):

    signed_short = (high_byte << 8) | low_byte

    return signed_short

def get_acceleration_data(ser):

    # Read 11 bytes of data from the serial port.
    hex_data = ser.readline(11)

    if hex_data[0] == '0x55' and hex_data[1] == '0x51':

        # Extract the acceleration data from the hexadecimal data.
        x_acceleration = convert_to_signed_short(hex_data[2], hex_data[3])
        y_acceleration = convert_to_signed_short(hex_data[4], hex_data[5])
        z_acceleration = convert_to_signed_short(hex_data[6], hex_data[7])

        return x_acceleration, y_acceleration, z_acceleration

ser = serial.Serial('COM6', 9600)

while True:
    if ser.readline
        x_acceleration, y_acceleration, z_acceleration = get_acceleration_data(ser)

    # Print the acceleration data.
    print('X acceleration:', x_acceleration)
    print('Y acceleration:', y_acceleration)
    print('Z acceleration:', z_acceleration)

ser.close()