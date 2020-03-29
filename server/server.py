import shared

import threading
import queue
import re
import requests
import json

from bottle import route, run, template, get, post, request, static_file, abort, Bottle
import gevent
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


class Server(threading.Thread):
    app = Bottle()
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.running = True
        self.app.route('/ws', callback=self.handleWebsocket)


    def run(self):
        WSGIServer(('0.0.0.0', 8000), self.app, handler_class=WebSocketHandler).serve_forever()


    def handleWebsocket(self):
        ws = request.environ.get('wsgi.websocket')
        if not ws:
            abort(400, 'Expected WebSocket Request!')
        print('WebSocket connected')
        while not ws.closed:
            try:
                ws.send(self.q.get(False))
            except Exception: pass
            try:
                m = ""
                with gevent.Timeout(0.1, False):
                    m = ws.receive()
                if not (m == None or m == ""):
                    pass # send this on to the Rover
            except WebSocketError: break


    @app.get("/test")
    def test():
        pass


    @app.get("/")
    @app.get('/<filepath:path>')
    def sendFile(filepath='index.html'):
        return static_file(filepath, root='../client/')
