import serial

checksum = 0
data = []
ser = serial.Serial('COM6', 9600)


# def read_byte(serial_device):
#     start_bit = serial_device.read()
#     return start_bit

acceleration_data = []
angular_velocity_data = []
angle_data = []
misc_data = []


# def new_data_line(serial_device):
#     new_data = [b'\x55']
#     new_byte = serial_device.read()
#     if new_byte == b'\x55':
#         new_data_line(serial_device)
#         return
#



try:
    new_data = [b'\x55']
    while True:
        new_byte = ser.read()
        if new_byte != b"\x55":
            new_data.append(new_byte)
        elif new_byte == b'\x55':
            if len(new_data) < 2:
                misc_data.append(new_data)
            elif new_data[1] == b'\x51':
                acceleration_data.append(new_data)
            elif new_data[1] == b'\x52':
                angular_velocity_data.append(new_data)
            elif new_data[1] == b'\x53':
                angle_data.append(new_data)
            new_data = [b'\x55']


except KeyboardInterrupt:
    ser.close()

for i in acceleration_data:
    print(i)