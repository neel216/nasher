import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Verification:
    def __init__(self, parent, menu, mainMenu, entryPage, selectionPage, objectID):
        self.verification = tk.Frame(master=parent)
        self.verification.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.verification.place(in_=parent, x=0, y=0, relwidth=1, relheight=1)
        self.mainMenu = mainMenu
        self.menu = menu
        self.entryPage = entryPage
        self.selectionPage = selectionPage

        restart = ttk.Button(self.verification, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, columnspan=2, sticky='w')

        
        title = tk.Label(self.verification, text='Verify OCR Value', font=tkFont.Font(size=30))
        title.grid(row=1, column=0, columnspan=2)

        prompt = tk.Label(self.verification, text='Is the object number correct?')
        prompt.grid(row=2, column=0, columnspan=2)

        number = tk.Label(self.verification, text=objectID)
        number.grid(row=3, column=0, columnspan=2)

        wrong = ttk.Button(self.verification, text='No', command=self.entryPage.show)
        correct = ttk.Button(self.verification, text='Yes', command=self.selectionPage.show)
        wrong.grid(row=4, column=0)
        correct.grid(row=4, column=1)


        self.verification.grid_columnconfigure([0, 1], weight=1)
        self.verification.grid_rowconfigure([1, 2, 3, 4], weight=1)

    def show(self):
        self.verification.lift()

    def hide(self):
        self.menu.lift()