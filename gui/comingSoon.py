import tkinter as tk
from tkinter import ttk


class ComingSoon:
    def __init__(self, parent, menu, mainMenu):
        self.soon = tk.Frame(master=parent)
        self.soon.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.mainMenu = mainMenu
        self.menu = menu
        self.parent = parent


        title = ttk.Label(self.soon, text='Feature Coming Soon!')
        title.grid(row=0, column=0)

        restart = ttk.Button(self.soon, text='Restart', command=self.hide)
        restart.grid(row=2, column=0)

        self.soon.grid_columnconfigure(0, weight=1)
        self.soon.grid_rowconfigure([0, 1, 2], weight=1)

    def show(self):
        self.soon.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.soon.lift()

    def hide(self):
        self.soon.pack_forget()
        self.menu.lift()
    
    def destroy(self):
        self.soon.destroy()