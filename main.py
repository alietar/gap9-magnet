import serial
import time

from gcode import *

# In mm
length = 10
width = 10
height = 10

nb_length = 5 # Number of points to measure lengthwise
nb_width = 5 # Number of points to measure widthwise
nb_height = 2 # Number of points to measure heightwise


print("--- Measure of electromagnetism for GAP9 ---")

port = input("Enter the machine's port (e.g. /dev/ttyUSB0): ")

machine = Machine(port, debug=False)

print("-> Move the speaker to the desired starting position")

user_input = ""
while(user_input != "start"):
    user_input = input("-> Write down 'start' when it's done: ")

machine.send("G92 X0 Y0 Z0") # Reset home coordinates
machine.send("G90") # Set coordinates to absolute
machine.send("G0 F2000") # Set speed


print("--- Starting the measures ---")

length_gap = length / (nb_length - 1)
width_gap = width / (nb_width - 1)
height_gap = height / (nb_height - 1)

for i in range(nb_height):
    z = height_gap * i
    for j in range(nb_length):
        x = length_gap * j

        for k in range(nb_width):
            y = length_gap * k
            machine.send(f"G0 X{str(x)} Y{str(y)} Z{str(z)}", wait=True)

machine.send(f"G0 X0 Y0 Z0")


machine.close()
