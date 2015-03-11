__author__ = 'JsAndPy'

from Config import *
import threading
import socket
import time

class SockClient4Py(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Init socket client
        self.__CLIENT_SOCKET = None
        self.__HOST = Config.HOST
        self.__PORT = Config.PORT
        self.__RECV_BUFFER = 4096        
        self.__MSG = ''
        self.__handleCallback = None

    def run(self):
        self.__creatSocket()

    def __creatSocket(self):
        # Reconnect to server when lost connection
        while True:
            time.sleep(0.01)
            # Start with a socket at 5-second timeout
            self.__CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__CLIENT_SOCKET.settimeout(5.0)

            # Check and turn on TCP Keepalive
            x = self.__CLIENT_SOCKET.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
            if x == 0:
                # Socket Keepalive off, turning on
                self.__CLIENT_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            try:
                self.__CLIENT_SOCKET.connect((self.__HOST, int(self.__PORT)))
                print('Connected to server - Host: ' + str(self.__HOST) + 'Port: ' + str(self.__PORT))
            except socket.error:
                continue

            # Start looping received data from server
            while True:
                time.sleep(0.01)
                try:
                    data = str(self.__CLIENT_SOCKET.recv(self.__RECV_BUFFER), 'utf8')
                    if data:
                        self.__MSG += data
                        if self.__MSG.find("#####") != -1:
                            substrings = self.__MSG[:self.__MSG.find('#####')]
                            self.__MSG = self.__MSG[self.__MSG.find('#####') + len('#####'):]
                            if substrings != '':
                                self.__handle(substrings)
                    else:
                        print('Other Socket err, exit and try creating socket again')
                        break
                except socket.timeout:
                    continue

                except:
                    print('Other Socket err, exit and try creating socket again')
                    break

            self.__CLIENT_SOCKET.close()

    def setCallBackHandle(self, callback):
        self.__handleCallback = callback

    def __handle(self, message):
        self.__handleCallback(message)

    def doSendData(self, message):
        msgRaw = str(message) + '#####'
        self.__CLIENT_SOCKET.send(bytes(msgRaw, 'utf8'))