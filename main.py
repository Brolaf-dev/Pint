import tkinter as tk
from Agenda import Agenda
from MedicineSchedule import MedicineSchedule
from MainMenu import MainMenu

class GuiController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.grid()

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

app = GuiController()
app.mainloop()
