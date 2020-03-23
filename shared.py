import queue

q_console = queue.Queue()
q_controls = queue.Queue()
q_server = queue.Queue()

thread_console = None
thread_controls = None
thread_server = None

app_name = 'Rover'

voltage = 0
