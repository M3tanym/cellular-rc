import queue
from threading import Thread

import gevent
from bottle import request, static_file, abort, Bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

from server import shared


class Server(Thread):
    app = Bottle()

    def __init__(self, q):
        super().__init__()
        self.q = q
        self.running = True
        self.app.route('/ws', callback=self.handle_ws)

    def run(self):
        WSGIServer(('0.0.0.0', 2343), self.app, handler_class=WebSocketHandler).serve_forever()

    def handle_ws(self):
        ws = request.environ.get('wsgi.websocket')
        if not ws:
            abort(400, 'Expected WebSocket Request!')
        print('WebSocket connected')
        with self.q.mutex:
            self.q.queue.clear()
        while not ws.closed:
            try:
                ws.send(self.q.get(False))
            except queue.Empty:
                pass
            try:
                m = ""
                with gevent.Timeout(0.1, False):
                    m = ws.receive()
                if not (m is None or m == ""):
                    # send this on to the Rover
                    shared.q_tcpsocket.put(m)
                    print('WS->TCP:', m)
            except WebSocketError:
                break

    @app.get("/test")
    def test(self=None):
        return 'test'

    @app.get("/")
    @app.get('/<filepath:path>')
    def send_file(self=None, filepath='index.html'):
        return static_file(filepath, root='../client/')
