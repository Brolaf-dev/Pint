import tkinter as tk
import socket
import sys

LARGE_FONT = ("Verdana", 12)
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('192.168.1.101',port))

class GuiController(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.grid()#pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainMenu, Agenda, MedicineSchedule):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0,columnspan=2)

        button = tk.Button(self, text="Visit Page 1",
                           command=lambda: controller.show_frame(Agenda))
        button.grid()

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(MedicineSchedule))
        button2.grid()


class Agenda(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = tk.Label(self, text="Agenda!!!", font=LARGE_FONT)
        titleLabel.grid(row=0,columnspan=7)
        dropDownMenuLabel = tk.Label(self, text="Choose month")
        dropDownMenuLabel.grid(row=1,columnspan=3)
        variable = tk.StringVar(self)
        variable.set("January")  # default value
        workingList = ["January", "February", "March","April","May","June","July","August","September","October","November","December"]
        dropDown = tk.OptionMenu(self, variable, *workingList,command=self.showMonth)#lambda variable: sys.stdout.write(variable+'\n'))
        dropDown.grid(row=1,column=3,columnspan=4)
        self.wid = []
        self.selectedDay = 0

        mainMenuButton = tk.Button(self, text="Main Menu",command=lambda: controller.show_frame(MainMenu))
        mainMenuButton.grid(row=15,columnspan=7)

    def showMonth(self, event):
        self.refresh()
        self.days=31
        self.columns=7
        if event in ["January", "March","May","July","August","October","December"]:
            self.days=31
        elif event in ["April", "June","September","November"]:
            self.days=30
        else:
            self.days=28
        self.rows=int(self.days/self.columns) if self.days%self.columns == 0 else int(self.days/self.columns)+1
        self.printedDays = 1
        for i in range(self.rows):
            for j in range(self.columns):
                button = tk.Button(self, text=str(self.printedDays),command=lambda d=self.printedDays,month=event:self.popup(d,month))
                self.wid.append(button)
                button.grid(row=i+2,column=j)
                self.printedDays +=1
                if self.printedDays == self.days+1:
                    break


    def popup(self,day,month):
        self.selectedDay = day
        self.w=showAgendaDay(self.master,self.selectedDay,self.getMonth(month))
        self.master.wait_window(self.w.top)

    def getMonth(argument):
        switcher = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }
        return switcher.get(argument)

    def refresh(self):
        for w in self.wid[:]:
            w.grid_forget()
            self.wid.remove(w)

class showAgendaDay(object):
    def __init__(self,master,selectedDay,month):
        top=self.top=tk.Toplevel(master)
        top.grab_set()
        self.l=tk.Label(top,text="Date: "+str(selectedDay))
        self.l.grid(row=0,columnspan=3)
        self.agendaDayEvents = [["Kapper","13:00","Doetinchem"],["School","12:00","Enschede"]]
        self.showEvents = []
        self.addItem=tk.Button(top,text='Add Event',command=lambda d=selectedDay:self.popup(d))
        self.addItem.grid(row=0,column=3)
        global s
        s.send(bytes(str(month)+","+str(selectedDay)),"utf-8")
        completeBuffer = []
        while True:
            receiving_buffer = s.recv(1024)
            if not receiving_buffer: break
            completeBuffer+= receiving_buffer

        self.orderInput(completeBuffer,self.agendaDayEvents)
        self.showDayEvents(self.agendaDayEvents)

    def orderInput(self, completeBuffer, agendaDayEvents):
        linesplit = completeBuffer.split('\n')
        numberOfLines = 0
        for i in linesplit:
            #agendaDayEvents.append([])
            agendaDayEvents.append[numberOfLines].append()
            numberOfLines += 1

    def showDayEvents(self, day):
        rowCounter = 0
        for i in self.agendaDayEvents :
            columnCounter = 0
            for j in i:
                l = tk.Label(self.top, text=j)
                self.showEvents.append(l)
                l.grid(row=rowCounter + 2, column=columnCounter)
                columnCounter += 1
            button = tk.Button(self.top, text="Delete", command=lambda r=rowCounter: self.deleteEvent(r))
            self.showEvents.append(button)
            button.grid(row=rowCounter + 2, column=columnCounter)
            rowCounter += 1

    def popup(self,day):
        self.selectedDay = day
        self.top.grab_release()
        self.w=addAgendaItem(self.selectedDay,self.agendaDayEvents)
        self.top.wait_window(self.w.top)
        self.top.grab_set()
        self.refreshDisplay()

    def deleteEvent(self,row):
        del self.agendaDayEvents[row]
        self.refreshDisplay()

    def refreshDisplay(self):
        for w in self.showEvents[:]:
            w.grid_forget()
            self.showEvents.remove(w)
        self.showDayEvents(self.agendaDayEvents)

    def cleanup(self):
        self.top.destroy()


class addAgendaItem(object):
    def __init__(self,selectedDay,agendaDayEvents):
        self.top=tk.Toplevel()
        self.top.wm_title("Add")
        self.top.grab_set()
        self.l=tk.Label(self.top,text="Adding Event on Date: "+str(selectedDay))
        self.l.grid(row=0,columnspan=4)

        self.eventLabel=tk.Label(self.top,text="Event: ")
        self.eventLabel.grid(row=1,column=0)
        self.eventEntry=tk.Entry(self.top)
        self.eventEntry.grid(row=1,column=1)

        self.hourVar = tk.IntVar(self.top)
        self.minuteVar = tk.IntVar(self.top)
        self.hourVar.set(0)  # default value
        self.minuteVar.set(0)
        self.hourList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        self.minuteList = [0,5,10,15,20,25,30,35,40,45,50,60]

        self.eventHourLabel=tk.Label(self.top,text="Hour: ")
        self.eventHourLabel.grid(row=2,column=0)
        self.dropDownHour = tk.OptionMenu(self.top, self.hourVar, *self.hourList)
        self.dropDownHour.grid(row=2, column=1)

        self.eventMinuteLabel=tk.Label(self.top,text="Minute: ")
        self.eventMinuteLabel.grid(row=2,column=2)
        self.dropDownMinute = tk.OptionMenu(self.top, self.minuteVar, *self.minuteList)
        self.dropDownMinute.grid(row=2, column=3)

        self.eventPlaceLabel = tk.Label(self.top, text="Place: ")
        self.eventPlaceLabel.grid(row=3, column=0)
        self.eventPlaceEntry = tk.Entry(self.top)
        self.eventPlaceEntry.grid(row=3, column=1)
        self.b=tk.Button(self.top,text='Save',command=lambda a=agendaDayEvents: self.cleanup(a))
        self.b.grid(row=20,columnspan=4)

    def cleanup(self,agendaDayEvents):
        global client_socket,clientaddress
        agendaEvent=[self.eventEntry.get(),str(self.hourVar.get())+" : " + str(self.minuteVar.get()),self.eventPlaceEntry.get()]
        agendaDayEvents.append(agendaEvent)
        self.top.destroy()

class MedicineSchedule(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(MainMenu))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(Agenda))
        button2.pack()


app = GuiController()
app.mainloop()