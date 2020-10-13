import socket
import threading
import time
from Calendar import *

DAYS = 7
TIMESLOTS = 16


class Server:
    HOST = '127.0.0.1'
    PORT = 27960
    agentCount = 0
    socket = None
    respondingClients = []
    connections = set()

    def __init__(self):
        self.main_calendar = Calendar(DAYS, TIMESLOTS)

    def listen_for_requests(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))

        print("awaiting connection")
        while True:
            self.socket.listen(1)
            conn, addr = self.socket.accept()
            print('connection from:'.format(addr))
            self.connections.add(conn)
            self.agentCount += 1
            print('new agent'.format(self.agentCount))
            worker_thread = threading.Thread(target=self.request_handler, args=[conn])
            worker_thread.start()

    def request_handler(self, conn):
        print('Processing new connection {}'.format(conn))
        while True:
            print('read')
            data = conn.recv(1024).decode()

            received_calendar = self.parse_string_to_calendar_array(data)

            print('Server-receive:', received_calendar)
            if self.main_calendar.is_other_calendar_empty(received_calendar):
                message = str(self.main_calendar.get_calendar())
            else:
                self.main_calendar.update_calendar(received_calendar)
                message = str(self.main_calendar.get_calendar())
            conn.sendall(message.encode())
            break

        self.connections.remove(conn)
        self.agentCount -= 1
        print('Removed an agent - current agent count: {}'.format(self.agentCount))
        conn.close()

    def parse_string_to_calendar_array(self, data):
        calendar = []
        b = data.replace("[[", "").replace("]]", "")
        for line in b.split('], ['):
            row = list(map(int, line.split(
                ',')))
            calendar.append(row)
        return calendar


server = Server()
server_thread = threading.Thread(target=server.listen_for_requests())
server_thread.deamon = True
server_thread.start()
