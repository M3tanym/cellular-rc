import shared

import serial
import threading
import queue
import time


class Controls(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.running = True
        self.port = '/dev/tty.usbmodem14201'
        self.ser = serial.Serial(self.port, 115200, timeout=1)

    def run(self):
        while self.running:
            line = self.ser.read(10)
            line = line.decode().strip()
            if line[0] == '<' and line [-1] == '>' and line[2] == ':':
                # valid so far
                if line[1] == 'v':
                    shared.voltage = float(line[3:-2])
                else:
                    pass # for now

    def left(self):
        self.ser.write(b'<s:16>')
    def center(self):
        self.ser.write(b'<s:128>')
    def right(self):
        self.ser.write(b'<s:240>')
    def forward(self):
        self.ser.write(b'<d:256>')
        time.sleep(0.3)
        self.ser.write(b'<d:75>')
    def stop(self):
        self.ser.write(b'<d:0>')
