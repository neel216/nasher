import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Selection:
    def __init__(self, parent, menu, mainMenu, location, objectID, lookup, width):
        self.lookup = lookup
        self.selection = tk.Frame(master=parent)
        self.selection.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.selection.place(in_=parent, x=0, y=0, relwidth=1, relheight=1)
        self.mainMenu = mainMenu
        self.menu = menu
        self.location = location

        restart = ttk.Button(self.selection, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        title = ttk.Label(self.selection, text='Select the correct painting')
        title.grid(row=1, column=0)

        self.options = tk.Listbox(self.selection, height=int(0.007 * width), font=tkFont.Font(size=int(0.02*width)))
        self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
        self.options.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.options.yview)

        c = 1
        self.paintings = self.lookup.get_info(objectID)
        for i in self.paintings:
            if type(i['dimensions']) == type(' '):
                dims = i['dimensions']
            else:
                dims = ' x '.join(str(d) for d in i['dimensions'])
            output = f"{i['objectID']}   in {i['room']} on {i['locationType']} {i['location']}. Dimensions (cm): {dims}"
            self.options.insert(c, output)
            c += 1

        self.options.grid(row=2, column=0, sticky='ew')
        self.scrollbar.grid(row=2, column=1, sticky='ns')

        select = ttk.Button(self.selection, text='Select', command=self.select)
        select.grid(row=3, column=0)

        self.selection.grid_columnconfigure(0, weight=1)
        self.selection.grid_rowconfigure([1, 3], weight=1)
    
    # callback bound to mouse-move event
    def mouse_move_callback(self, event):
        # use event.y with a previous remembered y value to determine
        # directions
        directions = 1 # just as an example, could also be -1

        # scroll the listbox vertically. 
        # to increase scrolling speed, either multiply counter by some value >1
        # or replace 'units' which means scroll 1 character in the current setting 
        # by 'pages' for larger steps. 'pages' should scroll the visible 
        # area of the listbox further.
        self.options.yview_scroll(directions, 'units')

    def select(self):
        selectedLine = self.options.curselection()[0]
        selectedID = self.paintings[selectedLine]
        self.mainMenu.select(selectedID)

    def show(self):
        self.selection.lift()

    def hide(self):
        self.menu.lift()