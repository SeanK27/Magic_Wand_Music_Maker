import time
import serial
import pywitmotion as wit

connected = False
baud = 115200

with serial.Serial("COM6", baud, timeout=5) as ser:
    s = ser.read()



    msgs_num = 0
    while msgs_num < 1000:
        start = time.time()
        s = ser.read_until(b'U')
        #q = wit.get_quaternion(msg)
        #q = wit.get_magnetic(msg)
        #q = wit.get_angle(s)
        q = wit.get_gyro(s)
        #q = wit.get_acceleration(msg)
        if q is not None:
            msgs_num = msgs_num+1
            print(q)