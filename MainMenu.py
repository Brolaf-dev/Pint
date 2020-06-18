import tkinter as tk
from Settings import LARGE_FONT,s

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        from MedicineSchedule import MedicineSchedule
        from Agenda import Agenda

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Connect to Baymax", font=LARGE_FONT)
        label.grid(row=0, columnspan=4)

        baymaxIPlabel = tk.Label(self, text="Baymax IP", font=LARGE_FONT)
        baymaxIPlabel.grid(row=1, column=0)
        self.baymaxIpEntry = tk.Entry(self)
        self.baymaxIpEntry.grid(row=1, column=1)

        baymaxPortlabel = tk.Label(self, text="Baymax Port", font=LARGE_FONT)
        baymaxPortlabel.grid(row=1, column=2)
        self.baymaxPortEntry = tk.Entry(self)
        self.baymaxPortEntry.grid(row=1, column=3)

        connectButton = tk.Button(self, text="Connect",command=self.connect)
        connectButton.grid(row=2, columnspan=4)

        self.button = tk.Button(self, text="Agenda",
                           command=lambda: controller.show_frame(Agenda))
        self.button.config(state='disable')
        self.button.grid(row=3, column=0, columnspan=2)

        self.button2 = tk.Button(self, text="Medicine schedule",
                            command=lambda: controller.show_frame(MedicineSchedule))
        self.button2.config(state='disable')
        self.button2.grid(row=3, column=2, columnspan=2)

    def connect(self):
        global s
        s.connect((self.baymaxIpEntry.get(),int(self.baymaxPortEntry.get())))
        self.button.config(state='active')
        self.button2.config(state='active')
