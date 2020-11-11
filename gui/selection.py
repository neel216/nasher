import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Selection:
    def __init__(self, parent, menu, mainMenu, lookup, width, location=None, objectID=None, rackPaintings=None):
        self.lookup = lookup
        self.selection = tk.Frame(master=parent)
        self.selection.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.mainMenu = mainMenu
        self.menu = menu
        self.location = location
        self.parent = parent

        restart = ttk.Button(self.selection, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        if rackPaintings == None and location != None and objectID != None:
            title = ttk.Label(self.selection, text='Select the correct painting')
            title.grid(row=1, column=0, columnspan=2)

            self.options = tk.Listbox(self.selection, height=int(0.015 * width), font=tkFont.Font(size=int(0.0165 * width)))
            self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
            self.options.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.options.yview)

            c = 1
            if self.lookup.object_exists(objectID):
                self.paintings = self.lookup.get_info(objectID)
                for i in self.paintings:
                    if type(i['dimensions']) == type(' '):
                        dims = i['dimensions']
                    else:
                        dims = ' x '.join(str(d) for d in i['dimensions'])
                    output = f"{i['objectID']} in {i['room']} on {i['location']}. Dimensions (cm): {dims}"
                    self.options.insert(c, output)
                    c += 1

                select = ttk.Button(self.selection, text='Select', command=self.select)
                select.grid(row=3, column=0, columnspan=2)
            else:
                self.options.insert(c, f'Found no results for object number {objectID}')
        elif rackPaintings != None and location == None and objectID == None:
            title = ttk.Label(self.selection, text='Rack Search Results')
            title.grid(row=1, column=0, columnspan=2)

            self.options = tk.Listbox(self.selection, height=int(0.015 * width), font=tkFont.Font(size=int(0.0165 * width)))
            self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
            self.options.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.options.yview)

            c = 1
            if len(rackPaintings) > 0:
                for i in rackPaintings:
                    if type(i['dimensions']) == type(' '):
                        dims = i['dimensions']
                    else:
                        dims = ' x '.join(str(d) for d in i['dimensions'])
                    output = f"{i['objectID']} in {i['room']} on {i['location']}. Dimensions (cm): {dims}"
                    self.options.insert(c, output)
                    c += 1
            else:
                self.options.insert(c, f'Found no results for that rack number')
        elif rackPaintings == None and location == None and objectID != None:
            title = ttk.Label(self.selection, text='Painting Search Results')
            title.grid(row=1, column=0, columnspan=2)

            self.options = tk.Listbox(self.selection, height=int(0.015 * width), font=tkFont.Font(size=int(0.0165 * width)))
            self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
            self.options.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.options.yview)

            c = 1
            if self.lookup.object_exists(objectID):
                self.paintings = self.lookup.get_info(objectID)
                for i in self.paintings:
                    if type(i['dimensions']) == type(' '):
                        dims = i['dimensions']
                    else:
                        dims = ' x '.join(str(d) for d in i['dimensions'])
                    output = f"{i['objectID']} in {i['room']} on {i['location']}. Dimensions (cm): {dims}"
                    self.options.insert(c, output)
                    c += 1
            else:
                self.options.insert(c, f'Found no results for object number {objectID}')

        self.options.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.scrollbar.grid(row=2, column=1, sticky='nse')

        up = ttk.Button(self.selection, text='Scroll up', command=lambda: self.options.yview_scroll(-1, tk.PAGES))
        up.grid(row=1, column=1, sticky='se')
        down = ttk.Button(self.selection, text='Scroll down', command=lambda: self.options.yview_scroll(1, tk.PAGES))
        down.grid(row=3, column=1, sticky='ne')

        self.selection.grid_columnconfigure(0, weight=1)
        self.selection.grid_rowconfigure([1, 3], weight=1)

    def select(self):
        selectedLine = self.options.curselection()[0]
        selectedID = self.paintings[selectedLine]
        self.mainMenu.select(selectedID)

    def show(self):
        self.selection.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.selection.lift()

    def hide(self):
        self.selection.pack_forget()
        self.menu.lift()
    
    def destroy(self):
        self.selection.destroy()