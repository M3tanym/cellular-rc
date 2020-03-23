import shared

import threading
import queue
import sys

class Console(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            s = input(shared.app_name + ' > ')
            if s == 'q':
                sys.exit()
            elif s == 'l':
                shared.thread_controls.left()
            elif s == 'c':
                shared.thread_controls.center()
            elif s == 'r':
                shared.thread_controls.right()
            elif s == 'f':
                shared.thread_controls.forward()
            elif s == 's':
                shared.thread_controls.stop()
            elif s == 'v':
                print(shared.voltage)
            else:
                print('unknown command ' + s)
