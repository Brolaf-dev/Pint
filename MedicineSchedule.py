import tkinter as tk
from Settings import LARGE_FONT


class MedicineSchedule(tk.Frame):
    def __init__(self, parent, controller):
        from MainMenu import MainMenu

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Medicine Schedule", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Main Menu",
                            command=lambda: controller.show_frame(MainMenu))
        button1.pack()