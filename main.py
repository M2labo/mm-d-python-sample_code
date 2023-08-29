import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)


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