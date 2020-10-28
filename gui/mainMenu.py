from gui import camera, verification, entry, selection, location, success
import tkinter as tk
from tkinter import ttk

class MainMenu:
    def __init__(self, parent):
        '''
        Creates and shows the main menu of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :return: returns nothing
        '''
        self.image = None
        self.objectID = ''
        self.selectedObjectID = ''
        self.lookup = None

        self.parent = parent
        self.mainMenu = tk.Frame(master=self.parent)
        self.mainMenu.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window

        self.success = success.Success(self.parent, self.mainMenu, self)
        self.location = location.Location(self.parent, self.mainMenu, self, self.success, self.selectedObjectID, self.lookup)
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.location, self.objectID)
        self.entry = entry.Entry(self.parent, self.mainMenu, self)
        self.verification = verification.Verification(self.parent, self.mainMenu, self, self.entry, self.selection, self.objectID)
        self.camera = camera.Camera(self.parent, self.mainMenu, self, self.verification)

        self.show()

    def show(self):
        button1 = ttk.Button(self.mainMenu, text='Change a Painting\'s Location', command=self.camera.show)
        button2 = ttk.Button(self.mainMenu, text='Lookup a Painting')
        button3 = ttk.Button(self.mainMenu, text='Lookup a Rack')
        button4 = ttk.Button(self.mainMenu, text='Scan a Rack')
        button5 = ttk.Button(self.mainMenu, text='Add a Painting')

        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0)
        button3.grid(row=2, column=0)
        button4.grid(row=3, column=0)
        button5.grid(row=4, column=0)

        self.mainMenu.grid_columnconfigure(0, weight=1)
        self.mainMenu.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)

        self.mainMenu.lift()

    def capture_image(self):
        self.image = self.camera.get_picture()
        self.objectID = '2016.19.1' # process image and get this from OCR

        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.success, self.objectID)
        self.verification = verification.Verification(self.parent, self.mainMenu, self, self.entry, self.selection, self.objectID)
        self.verification.show()

    def select(self, selectedObjectID, lookup):
        self.selectedObjectID = selectedObjectID
        self.lookup = lookup
        self.location = location.Location(self.parent, self.mainMenu, self, self.success, self.selectedObjectID, self.lookup)
        self.location.show()