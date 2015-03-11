__author__ = 'JsAndPy'

from Socket.SockServer4Py import *
import time

class Server:
    def __init__(self):
        self.SOCKET_SERVER = SockServer4Py()
        self.SOCKET_SERVER.start()

if __name__ == "__main__":
    s = Server()
    while True:
        time.sleep(1)
        s.SOCKET_SERVER.doBroadcastData({'id': 1, 'data': 'Hello World'})
