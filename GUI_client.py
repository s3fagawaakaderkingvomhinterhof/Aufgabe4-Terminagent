#############
# GUI CLASS #
#############

import wx
import wx.grid as gridlib
from Calendar import *
from logic_client import *
import math
import copy

import threading

days = 7
half_hours = 16

NEW_CALENDAR_STRING = 'CALENDAR:'


class ClientFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='Aufgabe-4: Terminagent Client')
        self.rows = half_hours
        self.columns = days
        self.edge_length = 39

        self.name_string = 'meeting'
        """
        self.dlg = wx.TextEntryDialog(self, 'Wie heißen Sie?', 'Eingabeformular')
        self.dlg.SetValue("Martin")
        if self.dlg.ShowModal() == wx.ID_OK:
            self.name_string = self.dlg.GetValue()
        self.dlg.Destroy()
        """
        ######################
        # define grid object #
        ######################
        self.grid = wx.grid.Grid(self, -1)

        self.grid.CreateGrid(self.rows + 1, self.columns)
        self.grid.SetRowLabelSize(55)

        self.grid.SetRowLabelValue(0, '08:00')
        self.grid.SetRowLabelValue(1, '08:30')
        self.grid.SetRowLabelValue(2, '09:00')
        self.grid.SetRowLabelValue(3, '09:30')
        self.grid.SetRowLabelValue(4, '10:00')
        self.grid.SetRowLabelValue(5, '10:30')
        self.grid.SetRowLabelValue(6, '11:00')
        self.grid.SetRowLabelValue(7, '11:30')
        self.grid.SetRowLabelValue(8, '12:00')
        self.grid.SetRowLabelValue(9, '12:30')
        self.grid.SetRowLabelValue(10, '13:00')
        self.grid.SetRowLabelValue(11, '13:30')
        self.grid.SetRowLabelValue(12, '14:00')
        self.grid.SetRowLabelValue(13, '14:30')
        self.grid.SetRowLabelValue(14, '15:00')
        self.grid.SetRowLabelValue(15, '15:30')
        self.grid.SetRowLabelValue(16, 'Aktionen')

        self.grid.SetColLabelSize(55)
        self.grid.SetColLabelValue(0, 'Montag')
        self.grid.SetColLabelValue(1, 'Dienstag')
        self.grid.SetColLabelValue(2, 'Mittwoch')
        self.grid.SetColLabelValue(3, 'Donnerstag')
        self.grid.SetColLabelValue(4, 'Freitag')
        self.grid.SetColLabelValue(5, 'Samstag')
        self.grid.SetColLabelValue(6, 'Sonntag')

        for i in range(0, self.columns):
            for j in range(0, self.rows):
                self.grid.SetCellBackgroundColour(j, i, wx.WHITE)
                self.grid.SetCellValue(j, i, ' ')

        self.grid.SetCellValue(16, 0, 'Sende Plan')
        self.grid.SetReadOnly(16, 0, True)

        self.grid.SetCellValue(16, 1, 'Löschen')
        self.grid.SetReadOnly(16, 1, True)

        self.grid.SetCellValue(16, 4, 'Dauer:')
        self.grid.SetReadOnly(16, 4, True)

        self.grid.SetCellValue(16, 5, '1')

        self.grid.SetCellValue(16, 6, 'Suche Termin')
        self.grid.SetReadOnly(16, 6, True)

        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.single_left_click)

        #################
        # other objects #
        #################
        self.HOST = '127.0.0.1'
        self.PORT = 27960
        self.s = None
        self.client_calendar_obj = Calendar(self.columns, self.rows)
        self.old_calendar_data = [-1]

        self.Centre()
        self.SetSize(
            (self.rows * self.edge_length + 7, self.columns * self.edge_length + 145))
        self.Show()

    def refresh_view(self):
        print('refresh')
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                if self.client_calendar_obj.is_timeslot_busy(i, j):
                    self.grid.SetCellValue(j, i, self.name_string)
                    self.grid.SetCellBackgroundColour(j, i, wx.RED)
                    self.grid.ForceRefresh()

    def toggle_free(self, x, y):
        self.grid.SetCellValue(y, x, self.name_string)
        self.grid.SetCellBackgroundColour(y, x, wx.RED)
        self.client_calendar_obj.toggle_timeslot_busy(x, y)

    def toggle_busy(self, x, y):
        self.grid.SetCellValue(y, x, ' ')
        self.grid.SetCellBackgroundColour(y, x, wx.WHITE)
        self.client_calendar_obj.toggle_timeslot_busy(x, y)

    def single_left_click(self, event):
        print('left click')
        pos = [event.GetCol(), event.GetRow()]
        self.toggle_color(pos)

    def toggle_color(self, pos):
        print(pos)
        if pos[1] == 16:
            if pos[0] == 0:
                print('click send button')

                diff_calendar = get_diff_of_current_and_old_calendar(self.client_calendar_obj.get_calendar(),
                                                                     self.old_calendar_data, self.columns,
                                                                     self.rows)

                print('diff beetween old an current:', diff_calendar)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.HOST, self.PORT))
                    s.sendall(str.encode(str(diff_calendar)))
                    response = s.recv(1024).decode()
                    print('received calendar:', response)

                    self.old_calendar_data = self.client_calendar_obj.calendar
                    print('old calendar:', self.old_calendar_data)

                    received_calendar = parse_string_to_calendar_array(response)
                    self.client_calendar_obj.calendar = received_calendar
                    print('current calendar:', self.client_calendar_obj.calendar)

                    self.refresh_view()

            elif pos[0] == 1:
                print('click clear button')
                self.client_calendar_obj.clear_calendar()
                self.client_calendar_obj.print_calendar()
                for i in range(0, self.columns):
                    for j in range(0, self.rows):
                        if self.grid.GetCellValue(j, i) == self.name_string:
                            self.grid.SetCellValue(j, i, ' ')
                            self.grid.SetCellBackgroundColour(j, i, wx.WHITE)
                            self.grid.ForceRefresh()

            elif pos[0] == 6:
                print('click serach meet')
                meeting_time = float(self.grid.GetCellValue(16, 5))
                slots_float = meeting_time / 0.5
                slots = math.ceil(slots_float)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.HOST, self.PORT))
                    s.sendall(str.encode(str([slots])))
                    response = s.recv(1024).decode()
                    print('received calendar:', response)
                    day = int(response[1])
                    slot = int(response[4])

                for i in range(0, slots):
                    self.grid.SetCellBackgroundColour(slot + i, day, wx.GREEN)
                    self.grid.ForceRefresh()

            else:
                pass
        elif self.grid.GetCellValue(pos[1], pos[0]) == ' ':
            print('toggle free')
            self.toggle_free(pos[0], pos[1])
        else:
            print('toggle busy')
            self.toggle_busy(pos[0], pos[1])


#################
# main function #
#################

if __name__ == '__main__':
    app = wx.App(0)
    frame = ClientFrame(None)

    app.MainLoop()
