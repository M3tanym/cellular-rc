import queue
import socket
from threading import Thread
from time import sleep

from vehicle import config, shared


class Connection(Thread):
    def __init__(self, q):
        super().__init__()
        self.q = q
        self.s = None
        self.connected = False
        self.running = True

    def run(self):
        while self.running:
            while not self.connected and self.running:
                print('Connecting to socket...')
                try:
                    self.connect()
                    self.connected = True
                    with self.q.mutex:
                        self.q.queue.clear()
                    print('Socket connected!')
                except Exception as e:
                    print(f'Failed to connect to socket! {e}')
                    sleep(1)

            try:
                data = self.s.recv(256)
                if len(data) == 0:
                    self.connected = False
                else:
                    data = data.decode().strip()
                    shared.q_controls.put(data)
            except socket.timeout:
                pass
            try:
                c = self.q.get_nowait()
                if c == 'q':
                    self.running = False
                else:
                    self.send(c)
            except queue.Empty:
                pass

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(0.001)
        self.s.connect(config.server)

    def send(self, data):
        x = bytes(str(data), 'utf-8')
        self.s.send(x)
