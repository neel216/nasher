import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Location:
    def __init__(self, parent, menu, mainMenu, success, painting, lookup, sheet):
        self.location = tk.Frame(master=parent)
        self.location.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.location.place(in_=parent, x=0, y=0, relwidth=1, relheight=1)
        self.mainMenu = mainMenu
        self.menu = menu
        self.success = success
        self.painting = painting
        self.lookup = lookup
        self.sheet = sheet
        

        restart = ttk.Button(self.location, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        title = ttk.Label(self.location, text='Enter the new rack')
        title.grid(row=1, column=0, columnspan=3)
        
        self.rack = tk.StringVar()
        self.entry = ttk.Entry(self.location, textvariable=self.rack, font=tkFont.Font(size=50))
        self.entry.grid(row=2, column=0, columnspan=3)

        self.selectionKeyboard()

        ok = ttk.Button(self.location, text='Ok', command=self.submitRack)
        ok.grid(row=8, column=0, columnspan=3)


        self.location.grid_columnconfigure([0, 1, 2], weight=1)
        self.location.grid_rowconfigure([1, 2, 8], weight=1)
        self.location.grid_rowconfigure([3, 4, 5, 6, 7], weight=1)

    def appendChar(self, char):
        i = len(self.rack.get())
        self.entry.insert(i, char)
    
    def deleteChar(self):
        i = len(self.rack.get()) - 1
        self.entry.delete(i)

    def selectionKeyboard(self):
        a = ttk.Button(self.location, text='A', command=lambda: self.appendChar('A'))
        b = ttk.Button(self.location, text='B', command=lambda: self.appendChar('B'))
        one = ttk.Button(self.location, text='1', command=lambda: self.appendChar('1'))
        two = ttk.Button(self.location, text='2', command=lambda: self.appendChar('2'))
        three = ttk.Button(self.location, text='3', command=lambda: self.appendChar('3'))
        four = ttk.Button(self.location, text='4', command=lambda: self.appendChar('4'))
        five = ttk.Button(self.location, text='5', command=lambda: self.appendChar('5'))
        six = ttk.Button(self.location, text='6', command=lambda: self.appendChar('6'))
        seven = ttk.Button(self.location, text='7', command=lambda: self.appendChar('7'))
        eight = ttk.Button(self.location, text='8', command=lambda: self.appendChar('8'))
        nine = ttk.Button(self.location, text='9', command=lambda: self.appendChar('9'))
        #period = ttk.Button(self.location, text='.', command=lambda: self.appendChar('.'))
        zero = ttk.Button(self.location, text='0', command=lambda: self.appendChar('0'))
        delete = ttk.Button(self.location, text='delete', command=self.deleteChar)

        a.grid(row=3, column=0)
        b.grid(row=3, column=2)
        one.grid(row=4, column=0)
        two.grid(row=4, column=1)
        three.grid(row=4, column=2)
        four.grid(row=5, column=0)
        five.grid(row=5, column=1)
        six.grid(row=5, column=2)
        seven.grid(row=6, column=0)
        eight.grid(row=6, column=1)
        nine.grid(row=6, column=2)
        #period.grid(row=7, column=0)
        zero.grid(row=7, column=1)
        delete.grid(row=7, column=2)

    def submitRack(self):
        self.sheet.add_rows([[self.painting['objectID'], self.painting['artist'], self.painting['otherInfo'], self.painting['room'] + ', ' + self.painting['location'], 'Nasher Painting Storage Room' + ', ' + self.rack.get()]])

        # update local data
        #self.lookup.edit_location(painting['index'], 'Nasher Painting Storage Room', self.rack.get())

        self.success.show()

    def show(self):
        self.location.lift()

    def hide(self):
        self.menu.lift()