from gui import camera, verification, entry, selection, location, success
import tkinter as tk
from tkinter import ttk
from tensorflow.keras.models import load_model
from ocr import process_ocr
from lookup import Lookup
from sheets import Sheet


class MainMenu:
    def __init__(self, parent, width, height):
        '''
        Creates and shows the main menu of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :return: returns nothing
        '''
        self.image = None
        self.objectID = ''
        self.selectedObjectID = ''
        self.lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')
        self.model = load_model('data/handwriting.model')
        self.sheet = Sheet('1cU243sy8jJz91GATvx_TfjWqdklvTCkbnQKEqDF3T8I', 'TMS Changes!A1:C')
        self.width = width
        self.height = height
        print('[INFO] Loaded model')

        self.parent = parent
        self.mainMenu = tk.Frame(master=self.parent)
        self.mainMenu.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        print('[INFO] Started GUI')

        self.success = success.Success(self.parent, self.mainMenu, self)
        print('[INFO] Loaded success screen')
        self.location = location.Location(self.parent, self.mainMenu, self, self.success, self.selectedObjectID, self.lookup, self.sheet, self.width)
        print('[INFO] Loaded location screen')
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.location, self.objectID, self.lookup, self.width)
        print('[INFO] Loaded selection screen')
        self.entry = entry.Entry(self.parent, self.mainMenu, self, self.width)
        print('[INFO] Loaded entry screen')
        self.verification = verification.Verification(self.parent, self.mainMenu, self, self.entry, self.selection, self.objectID)
        print('[INFO] Loaded verification screen')
        self.camera = camera.Camera(self.parent, self.mainMenu, self, self.verification)
        print('[INFO] Loaded camera screen')

        self.show()
        print('[INFO] Loaded main menu')

    def show(self):
        s = ttk.Style()
        fontSize = int(0.024 * self.width)
        padding = int(0.015*self.width)
        s.configure('TButton', font=('arial', fontSize), padding=padding)
        s.configure('TLabel', font=('arial', fontSize))
        s.configure('TEntry', font=('arial', fontSize))

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
        process_ocr(self.model, self.image)
        self.objectID = '2016.19.1' # process image and get this from OCR

        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.success, self.objectID, self.lookup, self.width)
        self.verification = verification.Verification(self.parent, self.mainMenu, self, self.entry, self.selection, self.objectID)
        self.verification.show()
    
    def correct_objectID(self, objectID):
        self.objectID = objectID

        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.success, self.objectID, self.lookup, self.width)
        self.selection.show()

    def select(self, selectedObjectID):
        self.selectedObjectID = selectedObjectID
        self.location = location.Location(self.parent, self.mainMenu, self, self.success, self.selectedObjectID, self.lookup, self.sheet, self.width)
        self.location.show()