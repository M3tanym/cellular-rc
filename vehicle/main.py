from vehicle import config, controls, shared, connection


def main():
    shared.thread_controls = controls.Controls(shared.q_controls)
    shared.thread_controls.daemon = True

    shared.thread_connection = connection.Connection(shared.q_connection)
    shared.thread_connection.daemon = True

    shared.thread_controls.start()

    shared.thread_connection.start()

    print(f'{config.app_name} running')
    shared.thread_controls.join()
    shared.thread_connection.join()


if __name__ == '__main__':
    main()
