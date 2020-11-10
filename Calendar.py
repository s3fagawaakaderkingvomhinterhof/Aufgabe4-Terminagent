class Calendar:
    def __init__(self, days, timeslots):
        self.days = days
        self.timeslots = timeslots
        self.calendar = [[0 for column in range(0, self.timeslots)] for row in range(self.days)]

    def set_calendar_entry(self, day, timeslot, value):  # change value of entry
        self.calendar[day][timeslot] = value

    def get_calendar_entry(self, day, timeslot):  # get value of entry
        return self.calendar[day][timeslot]

    def set_timeslot_busy(self, day, timeslot):  # set entry busy, set to 1
        self.set_calendar_entry(day, timeslot, 1)

    def undo_timeslot_busy(self, day, timeslot):  # set entry as free, set to 0
        self.set_calendar_entry(day, timeslot, 0)

    def is_timeslot_busy(self, day, timeslot):  # returns True if entry is busy
        return self.get_calendar_entry(day, timeslot) == 1

    def toggle_timeslot_busy(self, day, timeslot):  # toggle entry depends on value
        if not self.is_timeslot_busy(day, timeslot):
            self.set_timeslot_busy(day, timeslot)
        else:
            self.undo_timeslot_busy(day, timeslot)

    def print_calendar(self):  # prints full calendar
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                print(self.get_calendar_entry(day, timeslot), end='|')
            print()

    def get_calendar(self):  # returns full calendar
        return self.calendar

    def clear_calendar(self):  # clear calendar, own data model
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                self.undo_timeslot_busy(day, timeslot)

    def is_calendar_empty(self):  # check if own calendar is empty
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                if self.is_timeslot_busy(day, timeslot):
                    return False
        return True

    def overwrite_own_calendar(self, other_calendar):  # copy all entries from other to own calendar
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                self.set_calendar_entry(day, timeslot, other_calendar[day][timeslot])

    def is_other_calendar_empty(self, other_calendar):  # check if other calendar is empty
        for day in range(0, self.days):
            for timeslot in range(0, self.timeslots):
                if other_calendar[day][timeslot] == 1:
                    return False
        return True

    def is_calendar_different_to_own(self, other_calendar):  # checks if other calendar differs to own
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

    def get_meeting_list_for_day(self, other_calendar, day):  # returns list of compound meetings for given day
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

    def find_possible_slots(self, day):
        res = []
        for timeslot in range(0, self.timeslots):
            if not self.is_timeslot_busy(day, timeslot):
                res.append(timeslot)
        return res

    def is_current_meeting_free(self, list_of_possible_timeslots, temp_meeting):
        temp_meeting_is_possible = True
        for timeslot_ct in range(0, temp_meeting[1]):
            timeslot = temp_meeting[0]
            timeslot += timeslot_ct
            print(timeslot)
            if timeslot not in list_of_possible_timeslots:
                return False
            else:
                temp_meeting_is_possible and True
            print(temp_meeting_is_possible)

        return temp_meeting_is_possible

    def find_compound_slot(self, list_of_possible_timeslots, temp_meeting):  # add day as argument
        # insert code that tests if given temp_slot is free in own calendar then copy meeting to own
        if self.is_current_meeting_free(list_of_possible_timeslots, temp_meeting):
            print('TODO: func for copying temp meeting to own calendar')
            free = []
            for timeslot_ct in range(0, temp_meeting[1]):
                timeslot = temp_meeting[0]
                timeslot += timeslot_ct
                free.append(timeslot)
            return free
        else:
            number_of_slots = len(list_of_possible_timeslots)
            length_of_meeting = temp_meeting[1]
            res = []
            i = 0
            i_ink_start = 0
            while i < number_of_slots:
                res.append(list_of_possible_timeslots[i])
                i += 1
                print(res)
                if len(res) == length_of_meeting:
                    if (res[len(res) - 1] - res[0]) == (length_of_meeting - 1):
                        return res
                    else:
                        i_ink_start += 1
                        i = i_ink_start

                    res = []  # clear list after storing three elements

        return [-1]  # return if no slot of needed length is found

    def add_meeting_to_slot(self, possible_entry_pos, day, meeting):
        len_of_meeting = meeting[1]
        for entry in range(0, len_of_meeting):
            self.set_calendar_entry(day, possible_entry_pos[entry], 1)

    def add_meetings_from_calendar(self, other_calendar):
        for day in range(0, self.days):
            day_meetings_list = self.get_meeting_list_for_day(other_calendar, day)

            while len(day_meetings_list) > 0:
                temp_meeting = day_meetings_list.pop(0)
                possible_slots = self.find_possible_slots(day)
                possible_entry_pos = self.find_compound_slot(possible_slots,
                                                             temp_meeting)  # function have to prefer timeslot from temp_meeting
                self.add_meeting_to_slot(possible_entry_pos, day, temp_meeting)

        return True

    def update_calendar(self, other_calendar):
        if self.is_calendar_empty():
            print('calendar is empty')
            for i in range(0, self.days):
                for j in range(0, self.timeslots):
                    self.calendar[i][j] = other_calendar[i][j]  # use overwrite functions
            print('perform update on empty calendar')
        elif self.add_meetings_from_calendar(other_calendar):
            print('update_calendar: added meetings succesful')
        else:
            print('update_calendar: can not add meetings')
