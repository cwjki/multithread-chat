import sys
import threading
import zmq


class Client(object):

    def __init__(self, username):
        self.username = username
        self.context = zmq.Context()
        self.sock = None

    def handleConnect(self):
        self.sock = self.context.socket(zmq.REQ)
        self.sock.connect("tcp://localhost:" + '8080')

    def handleSend(self, message):
        data = {
            'nodeType': 'client',
            'username': username,
            'message': message,
        }
        self.sock.send_json(data)

    def run(self):
        self.handleConnect()

        while True:
            message = input("%s> " % username)
            self.handleSend(message)
            self.sock.recv()


if len(sys.argv) != 2:
    print("Correct usage: script, username")
    exit()

username = str(sys.argv[1])
client = Client(username)
client.run()
