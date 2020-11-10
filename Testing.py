free_slots_of_day = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def calc_timeslot_check_sum(start_slot, needed_length):
    sum = 0
    for i in range(start_slot, start_slot + needed_length):
        sum += i

    return sum

print(calc_timeslot_check_sum(7,3))

