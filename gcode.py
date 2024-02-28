import serial
import time
import sys

class Machine:
    def __init__(self, port, debug=False):
        self.debug = debug

        try:
            self.s = serial.Serial('/dev/ttyUSB0', 115200)
            print(f"Connected to the machine on {port}")
        except:
            print(f"Unabled to connect to the machine on {port}")
            print("Closing the program...")

            sys.exit()

        ### Wakes up the machine
        self.s.write(str.encode("\r\n\r\n"))
        time.sleep(2)
        self.s.flushInput()

        ### Setting the machine in millimeters
        self.send("G21")


    def send(self, code, wait=False):
        if wait:
            self.send_list([code, "G4 P0"])

        # Skip if the command is empty or is a comment
        if code.strip().startswith(';') or code.isspace() or len(code) <=0:
            pass
        else:
            self.print_user(f"Sending: {code}")
            self.s.write((code+'\n').encode())

            while(1): # Wait until the former gcode has been completed.
                grbl_out = self.s.readline()
                grbl_response = grbl_out.strip().decode('utf-8')

                self.print_user(f"Response: {grbl_response}")

                if grbl_response.startswith("ok"):
                    break


    def send_list(self, code_list, wait=False):
        if wait:
            code_list.append("G4 P0")

        for code in code_list:
            self.send(code)


    def listen(self):
        while(1): # Wait until the former gcode has been completed.
            grbl_out = self.s.readline()
            grbl_response = grbl_out.strip().decode('utf-8')

            self.print_user(f"Response: {grbl_response}")

            if grbl_response.startswith("ok"):
                break


    def print_user(self, msg):
        if self.debug:
            print(msg)


    def close(self):
        self.s.close()
