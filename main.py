import serial
import time
import platform

port = 'COM3'
baudrate = 115200

ser = serial.Serial()
ser.port = port
ser.baudrate = baudrate
ser.timeout = 1

if platform.system() == 'Windows':
    ser.setDTR(False)
    ser.setRTS(False)
ser.open()

# joystick
# left:center:right 0~63:64~127
# up:center:down 0~63:64~127
# speed 0~100

#front
ser.write(bytes([250, 0, 63, 0]))
time.sleep(1)

#right
ser.write(bytes([250, 50, 127, 0]))
time.sleep(1)

#left
ser.write(bytes([250, 50, 0, 0]))
time.sleep(1)

#back
ser.write(bytes([250, 63, 127, 0]))
time.sleep(1)



# change mode
# joystick mode
ser.write(bytes([251, 0, 0, 0]))
time.sleep(1)

# pwm mode
ser.write(bytes([251, 1, 0, 0]))
time.sleep(1)


# serial mode
ser.write(bytes([251, 2, 0, 0]))
time.sleep(1)
