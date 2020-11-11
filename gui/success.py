import tkinter as tk
from tkinter import ttk


class Success:
    def __init__(self, parent, menu, mainMenu):
        self.success = tk.Frame(master=parent)
        self.success.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.mainMenu = mainMenu
        self.menu = menu
        self.parent = parent


        title = ttk.Label(self.success, text='Success')
        title.grid(row=0, column=0)

        message = ttk.Label(self.success, text='Data sent to registrar.')
        message.grid(row=1, column=0)

        restart = ttk.Button(self.success, text='Restart', command=self.hide)
        restart.grid(row=2, column=0)

        self.success.grid_columnconfigure(0, weight=1)
        self.success.grid_rowconfigure([0, 1, 2], weight=1)

    def show(self):
        self.success.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.success.lift()

    def hide(self):
        self.success.pack_forget()
        self.menu.lift()
    
    def destroy(self):
        self.success.destroy()