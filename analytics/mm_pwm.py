import serial
import time
import platform
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import pandas as pd

# windows port = 'COM3'

port_pwm = '/dev/ttyUSB0'
port_serial = '/dev/ttyUSB1'
baudrate = 115200

ser = serial.Serial()
ser.port = port_serial
ser.baudrate = baudrate
ser.timeout = 1

ser_pwm = serial.Serial()
ser_pwm.port = port_pwm
ser_pwm.baudrate = baudrate
ser_pwm.timeout = 1

if platform.system() == 'Windows':
    ser.setDTR(False)
    ser.setRTS(False)
    ser_pwm.setDTR(False)
    ser_pwm.setRTS(False)
ser.open()
ser_pwm.open()

## PWM check
ser.write(bytes([251, 1, 0, 0]))
time.sleep(1)

import csv
with open('data_pwm.csv', 'w') as f:
    writer = csv.writer(f)
    for j in range(3):
        for i in  range(-40, 41):            
            for k in range(-40, 41):
                ser_pwm.write(bytes([250, 40 + i, 40 + k, 40, 40, 40, 40, 40, 40]))
                
                if k == -40 or k == 40: 
                    for m in range(1000):
                        ser.readline()
                else:
                    for m in range(100):
                        ser.readline()

                for m in range(10):

                    left_wheel_speed= None
                    right_wheel_speed = None
                    while True:
                        datas = ser.readline().decode('utf-8').split(':')

                        if datas[0] == 'left_speed':
                            left_wheel_speed = int(datas[1])
                        elif datas[0] == 'right_speed':
                            right_wheel_speed = int(datas[1])
                        
                        if left_wheel_speed is not None and right_wheel_speed is not None:
                            break
                    steering = None
                    while True:
                        datas = ser.readline().decode('utf-8').split(':')
                        if datas[0] == 'steering':
                            steering = int(datas[1])
                        if steering is not None:
                            break
                print(i*10+1520,k*10+1520,j *50,left_wheel_speed,right_wheel_speed,steering)
                writer.writerow([i*10+1520,k*10+1520,j *50,left_wheel_speed,right_wheel_speed,steering,(left_wheel_speed+right_wheel_speed)/2])
        ser_pwm.write(bytes([250, 40, 40, 80, 40, 40, 40, 40, 40]))
        time.sleep(1)
        ser_pwm.write(bytes([250, 40, 40, 40, 40, 40, 40, 40, 40]))
        time.sleep(1)


df = pd.read_csv('data_pwm.csv', header=None, names=['i', 'k', 'j', 'left_wheel_speed', 'right_wheel_speed', 'steering', 'speed'])

def f(front_back, left_right):
    if front_back < 0:
        front_back = 130 + front_back
    if left_right < 0:
        left_right = 130 + left_right
    df_select = df.query('i==@front_back and k==@left_right') 
    print(df_select)
    y_data = df_select.T.to_numpy().tolist()[6]
    x_data = df_select.T.to_numpy().tolist()[5]
    return y_data, x_data

df_select = df.query('i==0 and k==0')
x = df_select.T.to_numpy().tolist()[5]
y = df_select.T.to_numpy().tolist()[6]

# Define initial parameters
init_amplitude = 0
init_frequency = 0

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
fig.canvas.set_window_title('MobileMover')
scat = ax.scatter(x, y, marker="o", c="r", s=30, lw=0.5)
ax.set_xlabel('Steering')
ax.set_ylabel('Throttle')
ax.set_xlim([350, 1450])
ax.set_ylim([0, 2])
ax.grid(True)
ax.set_title('Steering vs Throttle')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
left_right_slider = Slider(
    ax=axfreq,
    label='left_right',
    valmin=-66,
    valmax=63,
    valinit=init_frequency,
    valstep=3
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
front_back_slider = Slider(
    ax=axamp,
    label="front_back",
    valmin=-66,
    valmax=63,
    valinit=init_amplitude,
    orientation="vertical",
    valstep=3
)


# The function to be called anytime a slider's value changes
def update(val):
    y_data, x_data = f(front_back_slider.val, left_right_slider.val)
    x.append(x_data)
    y.append(y_data)
    scat.set_offsets(np.c_[x_data, y_data])
    fig.canvas.draw_idle()


# register the update function with each slider
left_right_slider.on_changed(update)
front_back_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    left_right_slider.reset()
    front_back_slider.reset()
button.on_clicked(reset)

plt.show()