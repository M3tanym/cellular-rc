import shared

import console
import controls
import server

def main():
    shared.thread_console = console.Console(shared.q_console)
    shared.thread_console.start()

    shared.thread_controls = controls.Controls(shared.q_controls)
    shared.thread_controls.daemon = True
    shared.thread_controls.start()

    thread_server = server.Server(shared.q_server)
    thread_server.daemon = True
    thread_server.start()

    # thread_console.join()
    # thread_controls.join()
    # thread_server.join()


if __name__ == '__main__':
    main()
