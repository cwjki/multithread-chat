import socket
import zmq
import time
import threading


class Server(object):

    def __init__(self):
        self.context = zmq.Context()
        self.chat_sock = None
        self.display_sock = None
        self.socket = None

    def bind_server_port(self):
        self.chat_sock = self.context.socket(zmq.REP)
        self.chat_sock.bind("tcp://*:8080")

        self.display_sock = self.context.socket(zmq.PUB)
        self.display_sock.bind("tcp://*:8081")

    def handleReceive(self):
        data = self.chat_sock.recv_json()
        print(data)
        username = data['username']
        message = data['message']
        return [username, message]

    def handleSend(self, username, message):
        data = {
            'username': username,
            'message': message,
        }
        self.chat_sock.send(b'\x00')
        self.display_sock.send_json(data)

    def run(self):
        self.bind_server_port()
        while True:
            username, message = self.handleReceive()
            thread = threading.Thread(
                target=self.handleSend, daemon=True, args=(username, message,))
            thread.start()


if '__main__' == __name__:
    server = Server()
    server.run()
