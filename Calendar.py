class Calendar:
    def __init__(self, days, timeslots):
        self.days = days
        self.timeslots = timeslots
        self.calendar = [[0 for column in range(0, self.timeslots)] for row in range(self.days)]

    def set_timeslot_busy(self, day, timeslot):
        self.calendar[day][timeslot] = 1

    def undo_timeslot_busy(self, day, timeslot):
        self.calendar[day][timeslot] = 0

    def is_timeslot_busy(self, day, timeslot):
        return self.calendar[day][timeslot] == 1

    def toggle_timeslot_busy(self, day, timeslot):
        if not self.is_timeslot_busy(day, timeslot):
            self.set_timeslot_busy(day, timeslot)
        else:
            self.undo_timeslot_busy(day, timeslot)

    def print_calendar(self):
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                print(self.calendar[day][timeslot], end='|')
            print()

    def get_calendar(self):
        return self.calendar

    def clear_calendar(self):
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                self.undo_timeslot_busy(day, timeslot)

    def is_calendar_empty(self):
        for i in range(0, self.days):
            for j in range(0, self.timeslots):
                if self.is_timeslot_busy(i, j):
                    return False
        return True

    def overwrite_own_calendar(self, other_calendar):
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                self.calendar[day][timeslot] = other_calendar[day][timeslot]

    def is_other_calendar_empty(self, other_calendar):
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                if other_calendar[day][timeslot] == 1:
                    return False
        return True

    def is_calendar_different_to_own(self, other_calendar):
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                if self.calendar[day][timeslot] != other_calendar[day][timeslot]:
                    return True
        return False

    def pack_meetings(self, dates):
        size = len(dates)
        res = []
        for i in range(size):
            temp = dates[i]
            if len(res) == 0:
                res.append(temp)
            else:
                if temp[0] == res[len(res) - 1][0]:
                    res[len(res) - 1][1] += 1  # count up timeslots for one day
                else:
                    res.append(temp)  # add new timeslot for other day
        return res

    def scan_calendar_for_meetings(self, other_calendar):
        dates = []
        for i in range(0, self.days):
            for j in range(0, self.timeslots):
                if other_calendar[i][j] == 1:
                    dates.append([i, j])
        return self.pack_meetings(dates)

    def get_list_of_compund_day_meetings(self, other_calendar, day):
        compound_meetings = []
        for i in range(0, self.timeslots):
            if other_calendar[day][i] == 1:
                start_timeslot = i
                if len(compound_meetings) == 0:
                    compound_meetings.append([start_timeslot, 1])
                elif len(compound_meetings) > 0:
                    if (compound_meetings[len(compound_meetings) - 1][0] + compound_meetings[len(compound_meetings) \
                                                                                             - 1][1]) == i:
                        compound_meetings[len(compound_meetings) - 1][1] += 1
                    else:
                        compound_meetings.append([start_timeslot, 1])

        return compound_meetings

    def get_free_slot(self, other_calendar, day, slot_needed):
        slot_counter = 0
        slot_list = []
        found = False
        print('other calendar:', other_calendar[day])
        for timeslot in range(self.timeslots):
            if other_calendar[day][timeslot] == 0:
                slot_counter += 1
                slot_list.append(timeslot)
                if slot_needed == 1:
                    print('1-found')
                    return slot_list
                elif (slot_counter == slot_needed):
                    # if ((slot_list[len(slot_list)-1] - slot_list[0]) == slot_needed-1):
                    print('2-found')
                    return slot_list
                elif slot_counter >= slot_needed:
                    # slot_list.pop(0)
                    if ((slot_list[len(slot_list) - 1] - slot_list[0]) == (slot_needed - 1)):
                        print('3-found')
                    else:
                        print('4-found')
                        slot_list.pop(0)
                        return slot_list
        return [-1]

    def find_timeslot(self, other_calendar):  # besser wenn server immer alles durchguckt wo platz
        compound_slots_free = True
        for day in range(0, self.days):
            all_meetings = self.get_list_of_compund_day_meetings(other_calendar,
                                                                 day)  # speichert alle Termine des tages in Liste
            while len(all_meetings) > 0:
                temp_meeting = all_meetings.pop(0)

                for len_of_temp_meet in range(0, temp_meeting[1]):
                    compound_slots_free = compound_slots_free and not self.is_timeslot_busy(day, temp_meeting[
                        0] + len_of_temp_meet)
                if compound_slots_free:
                    for j in range(0, temp_meeting[1]):
                        self.set_timeslot_busy(day, temp_meeting[0] + j)
                else:
                    print('compound slot not free')

        return False

    def update_calendar(self, other_calendar):
        if self.is_calendar_empty():
            print('calendar is empty')
            for i in range(0, self.days):
                for j in range(0, self.timeslots):
                    self.calendar[i][j] = other_calendar[i][j]  # write better code with getter and setter functions
            print('perform update on empty calendar')
        elif self.find_timeslot(other_calendar):
            print('update_calendar: timeslot found')
        else:
            print('update_calendar: not possible')
