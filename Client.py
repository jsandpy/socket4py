__author__ = 'JsAndPy'

from Socket.SockClient4Py import *

class Client:
    def __init__(self):
        self.SOCKET_CLIENT = SockClient4Py()
        self.SOCKET_CLIENT.setCallBackHandle(self.showMessage)
        self.SOCKET_CLIENT.start()

    def showMessage(self, message):
        print('Messge: ' + str(message))

if __name__ == "__main__":
    c = Client()

