from threading import Thread

import queue
import serial
from time import sleep

from vehicle import config, shared


class Controls(Thread):
    def __init__(self, q):
        super().__init__()
        self.q = q
        self.ser = None
        self.running = True
        self.connected = False

    def run(self):
        while self.running:
            while not self.connected and self.running:
                try:
                    print('Connecting to serial...')
                    self.ser = serial.Serial(config.usb_port, 115200, timeout=0.01)
                    self.connected = True
                    with self.q.mutex:
                        self.q.queue.clear()
                    print('Serial connected!')
                except Exception as e:
                    print(f'Failed to connect to serial! {e}')
                    shared.quit_app('Serial')

            try:
                line = self.ser.read(10)
                line = line.decode().strip()
                if len(line) > 4 and line[0] == '<' and line[-1] == '>' and line[2] == ':':
                    # valid so far
                    if line[1] == 'v':
                        shared.voltage = float(line[3:-2])
                        shared.q_connection.put(f'{shared.voltage}\n')
                    else:
                        pass
                        # for now
            except Exception as e:
                self.running = False
                shared.quit_app(e)
            try:
                c = self.q.get_nowait()
                if c == 'q':
                    self.running = False
                else:
                    data = bytes(c, 'utf-8')
                    self.write(data)
            except queue.Empty:
                pass

    def write(self, command):
        self.ser.write(command)

    def left(self):
        self.ser.write(b'<s:-128>')

    def center(self):
        self.ser.write(b'<s:0>')

    def right(self):
        self.ser.write(b'<s:128>')

    def forward(self):
        self.ser.write(b'<d:64>')
        # time.sleep(0.3)
        # self.ser.write(b'<d:160>')

    def backward(self):
        self.ser.write(b'<d:-64>')

    def stop(self):
        self.ser.write(b'<d:0>')
