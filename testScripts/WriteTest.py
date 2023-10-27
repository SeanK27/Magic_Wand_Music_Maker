import time
import serial
import pywitmotion as wit

connected = False
baud = 9600

# Create serial object
ser = serial.Serial("COM6", baud, timeout=5)

# Send the command to enter calibration mode
ser.write(b'\xFF\xAA\x01\x01')

# Wait for the IMU to respond
ser.flush()
response = ser.readline()

# Check the response
print(response)
print(" ")

# Send the command to exit calibration mode
ser.write(b'\xFF\xAA\x01\x00')

# Wait for response
ser.flush()
response = ser.readline()

# Wait for Response
print(response)
# Close serial port
ser.close()