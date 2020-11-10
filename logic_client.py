import time
import socket


#########################
# Logic Class of Client #
#########################

def parse_string_to_calendar_array(data):
    calendar = []
    b = data.replace("[[", "").replace("]]", "")
    for line in b.split('], ['):
        row = list(map(int, line.split(
            ',')))
        calendar.append(row)
    return calendar


def get_diff_of_current_and_old_calendar(current_calendar, old_calendar, days, timeslots):
    temp = current_calendar
    if old_calendar[0] != -1:
        for day in range(0, days):
            for timeslot in range(0, timeslots):
                if old_calendar[day][timeslot] == 1:
                    temp[day][timeslot] = 0 # work on reference will still remove current meetings

        return temp
    else:
        return temp


def synchronize_calendar(ct=0):                                     # TODO: response have to be stored
    empty_cal = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    while True:
        ct += 1
        time.sleep(3.5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 27960))
            s.sendall(str.encode(
                str(empty_cal)))
            response = s.recv(1024).decode()
            print('t-res:', response)
