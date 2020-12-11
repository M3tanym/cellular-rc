import queue

from server import shared
import socket
from threading import Thread


class TCPSocket(Thread):
    def __init__(self, q):
        super().__init__()
        self.q = q
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(0.1)
        self.server.bind(('', 2342))
        self.server.listen(1)
        self.client = None
        self.running = True

    def run(self):
        while self.running:
            try:
                if not self.client:
                    self.client, address = self.server.accept()
                    self.client.settimeout(0.001)
                    print('TCPSocket connected')
                    with self.q.mutex:
                        self.q.queue.clear()
                if self.client:
                    data = self.client.recv(256)
                    data = data.decode().strip()
                    if len(data) == 0:
                        self.client = None
                    else:
                        shared.q_webserver.put(data)
                        print('TCP->WS:', data)
            except socket.timeout:
                pass
            try:
                data = self.q.get_nowait()
                if self.client:
                    self.client.send(bytes(str(data), 'utf-8'))
            except queue.Empty:
                pass
