#############
# GUI CLASS #
#############

import wx
import wx.grid as gridlib
import socket
from Calendar import *
from logic_client import *

days = 7
half_hours = 16

NEW_CALENDAR_STRING = 'CALENDAR:'


class ClientFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='Aufgabe-4: Terminagent Client')
        self.rows = half_hours
        self.columns = days
        self.edge_length = 39

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

        self.grid.SetCellValue(16, 0, 'Senden')
        self.grid.SetReadOnly(16, 0, True)

        self.grid.SetCellValue(16, 1, 'Löschen')
        self.grid.SetReadOnly(16, 1, True)

        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.single_left_click)

        #################
        # other objects #
        #################
        self.HOST = '127.0.0.1'
        self.PORT = 27960
        self.client_calendar_obj = Calendar(self.columns, self.rows)
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.Centre()
        self.SetSize(
            (self.rows * self.edge_length + 7, self.columns * self.edge_length + 145))
        self.Show()

    def single_left_click(self, event):
        print('left click')
        pos = [event.GetCol(), event.GetRow()]
        self.toggle_color(pos)

    def toggle_color(self, pos):
        print(pos)
        if pos[1] == 16:
            if pos[0] == 0:
                print('click Senden Button')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.HOST, self.PORT))
                    s.sendall(str.encode(str(self.client_calendar_obj.get_calendar())))
                    response = s.recv(1024).decode()

                    received_calendar = parse_string_to_calendar_array(response)

                    if self.client_calendar_obj.is_calendar_different_to_own(received_calendar):
                        print('look for changes')
                        self.client_calendar_obj.overwrite_own_calendar(received_calendar)
                        for i in range(0, self.columns):
                            for j in range(0, self.rows):
                                if self.client_calendar_obj.is_timeslot_busy(i, j) == True:
                                    self.grid.SetCellValue(j, i, 'meeting')
                                    self.grid.SetCellBackgroundColour(j, i, wx.RED)
                                    self.grid.ForceRefresh()
                        # print(received_calendar)
                    else:
                        print('no changes')
                        print('TODO: nothing')
                        print(received_calendar)

            elif pos[0] == 1:
                print('click Löschen Button')
                self.client_calendar_obj.clear_calendar()
                self.client_calendar_obj.print_calendar()
                for i in range(0, self.columns):
                    for j in range(0, self.rows):
                        if self.grid.GetCellValue(j, i) == 'meeting':
                            self.grid.SetCellValue(j, i, ' ')
                            self.grid.SetCellBackgroundColour(j, i, wx.WHITE)
                            self.grid.ForceRefresh()
            else:
                pass
        elif self.grid.GetCellValue(pos[1], pos[0]) == ' ':
            print('toggle free')
            self.grid.SetCellValue(pos[1], pos[0], 'meeting')
            self.grid.SetCellBackgroundColour(pos[1], pos[0], wx.RED)
            self.client_calendar_obj.toggle_timeslot_busy(pos[0], pos[1])
            self.client_calendar_obj.print_calendar()
        else:
            print('toggle busy')
            self.grid.SetCellValue(pos[1], pos[0], ' ')
            self.grid.SetCellBackgroundColour(pos[1], pos[0], wx.WHITE)
            self.client_calendar_obj.toggle_timeslot_busy(pos[0], pos[1])
            self.client_calendar_obj.print_calendar()


#################
# main function #
#################

if __name__ == '__main__':
    app = wx.App(0)
    frame = ClientFrame(None)
    app.MainLoop()
