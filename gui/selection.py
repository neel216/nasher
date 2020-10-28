import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from lookup import Lookup


class Selection:
    def __init__(self, parent, menu, mainMenu, location, objectID):
        self.lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')
        self.selection = tk.Frame(master=parent)
        self.selection.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.selection.place(in_=parent, x=0, y=0, relwidth=1, relheight=1)
        self.mainMenu = mainMenu
        self.menu = menu
        self.location = location

        restart = ttk.Button(self.selection, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        title = tk.Label(self.selection, text='Select the correct painting', font=tkFont.Font(size=30))
        title.grid(row=1, column=0)

        self.options = tk.Listbox(self.selection, width=50, height=25)

        c = 1
        self.paintings = self.lookup.get_info(objectID)
        for i in self.paintings:
            output = f"{i['objectID']} in {i['room']} on {i['locationType']} {i['location']}"
            self.options.insert(c, output)
            c += 1

        self.options.grid(row=2, column=0)

        select = ttk.Button(self.selection, text='Select', command=self.select)
        select.grid(row=3, column=0)

        self.selection.grid_columnconfigure(0, weight=1)
        self.selection.grid_rowconfigure([1, 3], weight=1)
    
    def select(self):
        selectedLine = self.options.curselection()[0]
        selectedID = self.paintings[selectedLine]
        self.mainMenu.select(selectedID, self.lookup)

    def show(self):
        self.selection.lift()

    def hide(self):
        self.menu.lift()