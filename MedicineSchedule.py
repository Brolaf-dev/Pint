import tkinter as tk
from Settings import LARGE_FONT,s,HEADERSIZE


class MedicineSchedule(tk.Frame):
    def __init__(self, parent, controller):
        from MainMenu import MainMenu

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Medicine Schedule", font=LARGE_FONT)
        label.grid(row=0,columnspan=2)

        variable = tk.StringVar(self)
        variable.set("Monday")  # default value
        workingList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saterday", "Sunday"]

        dropDown = tk.OptionMenu(self, variable, *workingList,
                                 command=self.showDay)  # lambda variable: sys.stdout.write(variable+'\n'))
        dropDown.grid(row=1,columnspan=2)

        mainMenuButton = tk.Button(self, text="Main Menu", command=lambda: controller.show_frame(MainMenu))
        mainMenuButton.grid(row=15, columnspan=2)

    def showDay(self, event):
        self.selectedDay = event
        self.w = showMedicineScheduleDay(self.master, self.selectedDay)
        self.master.wait_window(self.w.top)

class showMedicineScheduleDay(object):
    def __init__(self, master, selectedDay):
        top = self.top = tk.Toplevel(master)
        top.grab_set()

        self.l = tk.Label(top, text=selectedDay)
        self.l.grid(row=0, columnspan=3)

        self.showEvents = []
        self.medicineSchedule = []

        self.addMedicine = tk.Button(top, text='Add Medicine', command=lambda d=selectedDay: self.popup(d))
        self.addMedicine.grid(row=0, column=3)

        self.save = tk.Button(top, text='Save', command=lambda d=selectedDay: self.cleanup(d))
        self.save.grid(row=50, columnspan=5)
        print(selectedDay)
        msg = selectedDay
        msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + bytes(msg,"utf-8")
        s.send(msg)

        completeBuffer = ''
        while True:
            receiving_buffer = s.recv(1024)
            if not receiving_buffer: break
            completeBuffer += receiving_buffer.decode('utf-8')

        self.orderInput(completeBuffer, self.medicineSchedule)
        self.showDayMedicine(self.medicineSchedule)

    def orderInput(self, completeBuffer, medicineSchedule):
        if completeBuffer != '':
            linesplit = completeBuffer.split('\n')
            for i in linesplit:
                temp = i.split(',', 1)[1]  # Remove irrelevent data
                medicineSchedule.append(temp.split(','))

    def showDayMedicine(self, day):
        rowCounter = 0
        for i in self.medicineSchedule:
            columnCounter = 0
            for j in i:
                l = tk.Label(self.top, text=j)
                self.showEvents.append(l)
                l.grid(row=rowCounter + 2, column=columnCounter)
                columnCounter += 1
            button = tk.Button(self.top, text="Delete", command=lambda r=rowCounter: self.deleteEvent(r))
            button.grid(row=rowCounter + 2, column=columnCounter)
            self.showEvents.append(button)
            rowCounter += 1

    def popup(self, day):
        self.top.grab_release()
        self.selectedDay = day

        self.w = addAgendaItem(self.selectedDay, self.medicineSchedule)
        self.top.wait_window(self.w.top)

        self.top.grab_set()
        self.refreshDisplay()

    def deleteEvent(self, row):
        del self.medicineSchedule[row]
        self.refreshDisplay()

    def refreshDisplay(self):
        for w in self.showEvents[:]:
            w.grid_forget()
            self.showEvents.remove(w)
        self.showMedicineScheduleDay(self.medicineSchedule)

    def rchop(self, string, ending):
        if string.endswith(ending):
            return string[:-len(ending)]
        return string

    def cleanup(self, day):
        msg = ''
        for i in self.medicineSchedule:
            msg += str(day)
            for j in i:
                msg += ',' + str(j)
            msg += '\n'

        msg = self.rchop(msg, '\n')
        msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + bytes(msg, "utf-8")
        s.send(msg)

        self.top.destroy()

class addAgendaItem(object):
    def __init__(self, selectedDay, medicineSchedule):
        self.top = tk.Toplevel()
        self.top.wm_title("Add")
        self.top.grab_set()

        self.l = tk.Label(self.top, text="Adding Event on Date: " + str(selectedDay))
        self.l.grid(row=0, columnspan=4)

        self.medicineLabel = tk.Label(self.top, text="Medicine: ")
        self.medicineLabel.grid(row=1, column=0)
        self.medicineEntry = tk.Entry(self.top)
        self.medicineEntry.grid(row=1, column=1)

        self.hourVar = tk.IntVar(self.top)
        self.minuteVar = tk.IntVar(self.top)
        self.hourVar.set(0)  # default value
        self.minuteVar.set(0)
        self.hourList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        self.minuteList = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60]

        self.eventHourLabel = tk.Label(self.top, text="Hour: ")
        self.eventHourLabel.grid(row=2, column=0)
        self.dropDownHour = tk.OptionMenu(self.top, self.hourVar, *self.hourList)
        self.dropDownHour.grid(row=2, column=1)

        self.eventMinuteLabel = tk.Label(self.top, text="Minute: ")
        self.eventMinuteLabel.grid(row=2, column=2)
        self.dropDownMinute = tk.OptionMenu(self.top, self.minuteVar, *self.minuteList)
        self.dropDownMinute.grid(row=2, column=3)

        self.drawList = [1, 2, 3, 4, 5, 6]
        self.drawVar.set(1)
        self.drawLabel = tk.Label(self.top, text="Draw: ")
        self.drawPlaceLabel.grid(row=3, column=0)
        self.dropDownDraw = tk.OptionMenu(self.top, self.drawVar, *self.drawList)
        self.dropDownDraw.grid(row=2, column=1)

        self.b = tk.Button(self.top, text='Save', command=lambda a=medicineSchedule: self.cleanup(a))
        self.b.grid(row=20, columnspan=4)

    def cleanup(self, medicineSchedule):
        medicineAdd = [self.medicineEntry.get(), str(self.hourVar.get()) + " : " + str(self.minuteVar.get()),
                       self.drawVar.get()]
        medicineSchedule.append(medicineAdd)
        self.top.destroy()