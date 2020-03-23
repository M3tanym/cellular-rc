import shared

import threading
import queue

class Server(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            pass
