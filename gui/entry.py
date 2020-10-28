import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


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

        title = tk.Label(self.entry, text='Enter the correct object number', font=tkFont.Font(size=30))
        title.grid(row=1, column=0, columnspan=3)

        self.object_id = tk.StringVar()
        self.entryBox = ttk.Entry(self.entry, textvariable=self.object_id)
        self.entryBox.grid(row=2, column=0, columnspan=3)

        self.entryKeyboard()

        ok = ttk.Button(self.entry, text='Ok', command=self.correct_object_id)
        ok.grid(row=7, column=0, columnspan=3)

        self.entry.grid_columnconfigure([0, 1, 2], weight=1)
        self.entry.grid_rowconfigure([1, 2, 7], weight=1)
        self.entry.grid_rowconfigure([3, 4, 5, 6], weight=1)

    def appendChar(self, char):
        i = len(self.object_id.get())
        print(self.object_id.get(), i, char)
        self.entryBox.insert(i, char)
    
    def deleteChar(self):
        i = len(self.object_id.get()) - 1
        print(i)
        self.entryBox.delete(i)

    def entryKeyboard(self):
        one = ttk.Button(self.entry, text='1', command=lambda: self.appendChar('1'))
        two = ttk.Button(self.entry, text='2', command=lambda: self.appendChar('2'))
        three = ttk.Button(self.entry, text='3', command=lambda: self.appendChar('3'))
        four = ttk.Button(self.entry, text='4', command=lambda: self.appendChar('4'))
        five = ttk.Button(self.entry, text='5', command=lambda: self.appendChar('5'))
        six = ttk.Button(self.entry, text='6', command=lambda: self.appendChar('6'))
        seven = ttk.Button(self.entry, text='7', command=lambda: self.appendChar('7'))
        eight = ttk.Button(self.entry, text='8', command=lambda: self.appendChar('8'))
        nine = ttk.Button(self.entry, text='9', command=lambda: self.appendChar('9'))
        period = ttk.Button(self.entry, text='.', command=lambda: self.appendChar('.'))
        zero = ttk.Button(self.entry, text='0', command=lambda: self.appendChar('0'))
        delete = ttk.Button(self.entry, text='delete', command=self.deleteChar)

        one.grid(row=3, column=0)
        two.grid(row=3, column=1)
        three.grid(row=3, column=2)
        four.grid(row=4, column=0)
        five.grid(row=4, column=1)
        six.grid(row=4, column=2)
        seven.grid(row=5, column=0)
        eight.grid(row=5, column=1)
        nine.grid(row=5, column=2)
        period.grid(row=6, column=0)
        zero.grid(row=6, column=1)
        delete.grid(row=6, column=2)

    def correct_object_id(self):
        self.mainMenu.correct_objectID(self.object_id.get())
        self.object_id.set('')
    
    def show(self):
        self.entry.lift()

    def hide(self):
        self.menu.lift()