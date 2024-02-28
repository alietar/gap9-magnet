import serial
import time

from gcode import *


length = 25
width = 25
height = 5

nb_length = 5 # Number of points to measure lengthwise
nb_width = 5 # Number of points to measure widthwise
nb_height = 2 # Number of points to measure heightwise

#commands = [, "G90", "G1 X10 F100", "G4 P0", "G1 X0 F100"]


print("--- Measure of electromagnetism for GAP9 ---")

machine = Machine("/dev/ttyUSB0", debug=False)

print("-> Move the speaker to the desired starting position")

user_input = ""
while(user_input != "start"):
    user_input = input("-> Write down 'start' when it's done: ")

machine.send("G92 X0 Y0 Z0") # Reset home coordinates
machine.send("G90") # Set coordinates to absolute
machine.send("G0 F500") # Set speed


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

machine.send(f"G0 X0 Y0")


machine.close()
