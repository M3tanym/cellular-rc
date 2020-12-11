from server import shared, webserver, tcpsocket


def main():
    shared.thread_webserver = webserver.Server(shared.q_webserver)
    shared.thread_webserver.daemon = True
    shared.thread_webserver.start()

    shared.thread_tcpsocket = tcpsocket.TCPSocket(shared.q_tcpsocket)
    shared.thread_tcpsocket.daemon = True
    shared.thread_tcpsocket.start()

    print('Server running')

    shared.thread_webserver.join()
    shared.thread_tcpsocket.join()


if __name__ == '__main__':
    main()
