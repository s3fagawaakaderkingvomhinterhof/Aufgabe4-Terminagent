from Calendar import *

calendar_main_obj = Calendar(7, 16)
calendar_main_obj.set_timeslot_busy(0, 1)
#calendar_main_obj.undo_timeslot_busy(1, 0)
#calendar_main_obj.toggle_timeslot_busy(0,1)
#calendar_obj.toggle_timeslot_busy(1, 5)
calendar_main_obj.print_calendar()
print('############################')

calendar_obj_2 = Calendar(7, 16)
calendar_obj_2.toggle_timeslot_busy(0, 1)
calendar_obj_2.toggle_timeslot_busy(0, 2)
calendar_obj_2.toggle_timeslot_busy(0, 3)

calendar_obj_2.toggle_timeslot_busy(0, 8)
calendar_obj_2.toggle_timeslot_busy(0, 9)
calendar_obj_2.toggle_timeslot_busy(0, 12)
calendar_obj_2.print_calendar()
calendar_obj_2.toggle_timeslot_busy(2, 1)
calendar_obj_2.toggle_timeslot_busy(2, 2)
calendar_obj_2.toggle_timeslot_busy(2, 3)
calendar_obj_2.toggle_timeslot_busy(2, 4)
print('############################')


calendar_main_obj.update_calendar(calendar_obj_2.get_calendar())
calendar_main_obj.print_calendar()

print('==================')
#print(calendar_main_obj.is_calendar_different_to_own(calendar_obj_2.get_calendar()))

print(calendar_main_obj.get_list_of_compund_day_meetings(calendar_obj_2.get_calendar(), 0))
