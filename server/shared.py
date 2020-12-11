import queue


q_webserver = queue.Queue()
q_tcpsocket = queue.Queue()

thread_webserver = None
thread_tcpsocket = None
