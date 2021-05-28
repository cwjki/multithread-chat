import sys
import threading
import zmq


class Display(object):

    def __init__(self):
        self.context = zmq.Context()
        self.sock = None
        self.port = '8081'

    def handleConnect(self):
        self.sock = self.context.socket(zmq.SUB)
        self.sock.setsockopt_string(zmq.SUBSCRIBE, '')
        self.sock.connect("tcp://localhost:" + self.port)

    def run(self):
        self.handleConnect()
        while True:
            data = self.sock.recv_json()
            username, message = data['username'], data['message']
            print('{}: {}'.format(username, message))


client = Display()
client.run()
