import tkinter as tk
from tkinter import ttk


class Entry:
    def __init__(self, parent, menu, mainMenu):
        self.entry = tk.Frame(master=parent)
        self.entry.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.entry.place(in_=parent, x=0, y=0, relwidth=1, relheight=1)
        self.mainMenu = mainMenu
        self.menu = menu

        restart = ttk.Button(self.entry, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')





    def show(self):
        self.entry.lift()

    def hide(self):
        self.menu.lift()