import socket
import threading
import time
from Calendar import *
from UserList import *

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
        self.user_list = UserList()
        self.res = None

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
        # print('Processing new connection {}'.format(conn))
        while True:
            print('read')
            data = conn.recv(1024).decode()
            print('receive:', data)
            print('len of rec data:', len(data))
            self.res = None
            if len(data) == 350:
                received_calendar = self.parse_string_to_calendar_array(data)
                message = None

                if self.main_calendar.is_other_calendar_empty(received_calendar):
                    message = str(self.main_calendar.get_calendar())
                    self.res = message
                else:
                    self.main_calendar.update_calendar(received_calendar)
                    message = str(self.main_calendar.get_calendar())
                    self.res = message

                print('send:', self.res)
            elif len(data) <= 4:                # case for booking a meeting
                print('do booking')
                found = False
                needed_slots = int(data[1])
                for day in range(0, self.main_calendar.days):
                    if not found:
                        free_slots_of_day = self.main_calendar.find_possible_slots(day)
                        print('day:', day , 'slots:', free_slots_of_day)
                        len_of_slots = len(free_slots_of_day)
                        #check_sum = 0
                        #current_sum = 0
                        for time_slot in range(0, (len_of_slots - needed_slots+1)):

                            check_sum = self.calc_timeslot_check_sum(free_slots_of_day[time_slot], needed_slots)
                            current_sum = self.calc_timeslot_current_sum(time_slot,needed_slots,free_slots_of_day)

                            print('chk-sum:', check_sum)
                            print('cur-sum:', current_sum)

                            if check_sum == current_sum:
                                found = True
                                print('start meet at:', free_slots_of_day[time_slot])
                                self.res = str([day, free_slots_of_day[time_slot]])

                            if found:
                                break

                    else:
                        break

            for connection in self.connections:
                connection.sendall(self.res.encode())
            break
        self.connections.remove(conn)
        self.agentCount -= 1
        print('Removed an agent - current agent count: {}'.format(self.agentCount))
        conn.close()

    def calc_timeslot_check_sum(self, start_slot, needed_length):
        sum = 0
        for i in range(start_slot, start_slot + needed_length):
            sum += i

        return sum

    def calc_timeslot_current_sum(self, start_slot, needed_length, free_slots):
        sum = 0
        for i in range(start_slot, (start_slot + needed_length)):
            sum += free_slots[i]

        return sum

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
