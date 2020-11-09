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
        self.screen = None
        self.screens = {'change_painting': self.delete_change_painting,
                        'lookup_painting': self.delete_lookup_painting,
                        'lookup_rack': self.delete_lookup_rack,
                        'scan_rack': self.delete_scan_rack,
                        'add_painting': self.delete_add_painting}
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


        self.show()
        print('[INFO] Loaded main menu')

    def show(self):
        s = ttk.Style()
        fontSize = int(0.024 * self.width)
        padding = int(0.015*self.width)
        s.configure('TButton', font=('arial', fontSize), padding=padding)
        s.configure('TLabel', font=('arial', fontSize))
        s.configure('TEntry', font=('arial', fontSize))

        button1 = ttk.Button(self.mainMenu, text='Change a Painting\'s Location', command=self.change_painting)
        button2 = ttk.Button(self.mainMenu, text='Lookup a Painting', command=self.lookup_painting)
        button3 = ttk.Button(self.mainMenu, text='Lookup a Rack', command=self.lookup_rack)
        button4 = ttk.Button(self.mainMenu, text='Scan a Rack', command=self.scan_rack)
        button5 = ttk.Button(self.mainMenu, text='Add a Painting', command=self.add_painting)

        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0)
        button3.grid(row=2, column=0)
        button4.grid(row=3, column=0)
        button5.grid(row=4, column=0)

        self.mainMenu.grid_columnconfigure(0, weight=1)
        self.mainMenu.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)

        self.mainMenu.lift()
    
    def refresh_screens(self):
        for function in self.screens:
            if function == self.screen:
                self.screens[function]()

    def change_painting(self):
        self.refresh_screens()
        self.screen = 'change_painting'

        self.success = success.Success(self.parent, self.mainMenu, self)
        print('[INFO] Loaded success screen')
        self.location = location.Location(self.parent, self.mainMenu, self,
                                          success=self.success,
                                          painting=self.selectedObjectID,
                                          lookup=self.lookup,
                                          sheet=self.sheet,
                                          width=self.width)
        print('[INFO] Loaded location screen')
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, location=self.location, objectID=self.objectID)
        print('[INFO] Loaded selection screen')
        self.entry = entry.Entry(self.parent, self.mainMenu, self, self.width)
        print('[INFO] Loaded entry screen')
        self.verification = verification.Verification(self.parent, self.mainMenu, self, self.entry, self.selection, self.objectID)
        print('[INFO] Loaded verification screen')
        self.camera = camera.Camera(self.parent, self.mainMenu, self, self.verification)
        print('[INFO] Loaded camera screen')
    
        self.camera.show()
    
    def delete_change_painting(self):
        self.success.destroy()
        self.location.destroy()
        self.selection.destroy()
        self.entry.destroy()
        self.verification.destroy()
        self.camera.destroy()

    def lookup_painting(self):
        self.refresh_screens()
        self.screen = 'lookup_painting'
    
    def delete_lookup_painting(self):
        pass

    def lookup_rack(self):
        self.refresh_screens()
        self.screen = 'lookup_rack'

        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, objectID='2016.1.1')
        self.location = location.Location(self.parent, self.mainMenu, self,
                                          lookup=self.lookup,
                                          width=self.width,
                                          selection=self.selection)
        
        self.location.show()

    def delete_lookup_rack(self):
        self.selection.destroy()
        self.location.destroy()

    def scan_rack(self):
        self.refresh_screens()
        self.screen = 'scan_rack'

    def delete_scan_rack(self):
        pass

    def add_painting(self):
        self.refresh_screens()
        self.screen = 'add_painting'

    def delete_add_painting(self):
        pass

    def capture_image(self):
        self.image = self.camera.get_picture()
        process_ocr(self.model, self.image)
        self.objectID = '2016.19.1' # process image and get this from OCR

        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, location=self.location, objectID=self.objectID)
        self.verification = verification.Verification(self.parent, self.mainMenu, self, self.entry, self.selection, self.objectID)
        self.verification.show()
    
    def correct_objectID(self, objectID):
        self.objectID = objectID

        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, location=self.location, objectID=self.objectID)
        self.selection.show()

    def select(self, selectedObjectID):
        self.selectedObjectID = selectedObjectID
        self.location = location.Location(self.parent, self.mainMenu, self, self.success, self.selectedObjectID, self.lookup, self.sheet, self.width)
        self.location.show()
    
    def searchRackNumber(self, rackInfo):
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, rackPaintings=rackInfo)
        self.location.hide()
        self.selection.show()