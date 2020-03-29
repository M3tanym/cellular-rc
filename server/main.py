import shared
import server

def main():
    thread_server = server.Server(shared.q_server)
    thread_server.daemon = True
    thread_server.start()

    print('Server up on :8000')

    thread_server.join()

if __name__ == '__main__':
    main()
