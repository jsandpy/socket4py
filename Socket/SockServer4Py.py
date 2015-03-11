__author__ = 'JsAndPy'

import threading
import socket
import select

from Config import *

class SockServer4Py(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Init socket server
        self.__CONNECTION_LIST = [] # List socket connected
        self.__SERVER_SOCKET = None

        # Init config
        self.__HOST = Config.HOST
        self.__PORT = Config.PORT
        self.__RECV_BUFFER = 4096
        self.__MSG = ''
        self.__handleCallback = None

    def run(self):
        self.__creatSocket()

    def __creatSocket(self):
        #################################################################
        # init socket server
        self.__SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__SERVER_SOCKET.bind((self.__HOST, self.__PORT))
        self.__SERVER_SOCKET.listen(10)

        # Add server socket to the list of readable connections
        self.__CONNECTION_LIST.append(self.__SERVER_SOCKET)
        print("Server started on port " + str(self.__PORT))

        while True:
            #############################################################
            # server
            # Get the list sockets which are ready to be read through select
            read_sockets, write_sockets, error_sockets = select.select(self.__CONNECTION_LIST, [], [])

            for sock in read_sockets:
                # New connection
                if sock == self.__SERVER_SOCKET:
                    # __handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = self.__SERVER_SOCKET.accept()
                    self.__CONNECTION_LIST.append(sockfd)
                    print("Client (%s, %s) connected" % addr)

                # Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        # In Windows, sometimes when a TCP program closes abruptly,
                        # a "Connection reset by peer" exception will be thrown
                        data = str(sock.recv(self.__RECV_BUFFER), 'utf8')
                        if data:
                            self.__MSG += data
                            if self.__MSG.find("#####") != -1:
                                substrings = self.__MSG[:self.__MSG.find('#####')]
                                self.__MSG = self.__MSG[self.__MSG.find('#####') + len('#####'):]
                                if substrings != '':
                                    self.__handle(substrings)

                    except:
                        print("Client (%s, %s) is offline" % addr)
                        sock.close()
                        if sock in self.__CONNECTION_LIST:
                            self.__CONNECTION_LIST.remove(sock)

    def setCallBackHandle(self, callback):
        self.__handleCallback = callback

    def __handle(self, message):
        self.__handleCallback(message)

    # Function broadcast data to all client
    def doBroadcastData(self, message):
        # print("Send message: ", str(message))
        # Add message '#####' the finish message
        msgRaw = str(message) + '#####'

        # Do not send the message to master socket
        for socket in self.__CONNECTION_LIST:
            if socket != self.__SERVER_SOCKET:
                try:
                    socket.send(bytes(msgRaw, 'utf8'))
                except:
                    # Broken socket connection may be, chat client pressed ctrl+c for example
                    socket.close()
                    if socket in self.__CONNECTION_LIST:
                        self.__CONNECTION_LIST.remove(socket)