import queue

q_connection = queue.Queue()
q_controls = queue.Queue()

thread_connection = None
thread_controls = None

voltage = 0


def quit_app(reason):
    thread_connection.running = False
    thread_controls.running = False
    print(f'Exiting: {reason}')
