#!/usr/bin/env python3
# coding: utf-8

from gui import verification, entry, selection, location, success, comingSoon
import tkinter as tk
from tkinter import ttk
from lookup import Lookup
from sheets import Sheet
import camera_ocr


class MainMenu:
    '''
    Contains functions to create the main menu screen of the GUI,
    render and unrender screens of the GUI, and link together screens of the GUI
    '''
    def __init__(self, parent, width, height):
        '''
        Creates the main menu of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :param width: the width to make the frame
        :param height: the height to make the frame
        :return: returns nothing
        '''
        # Dictionary with function name keys and function values for to render and unrender screens as necessary
        self.screen = None
        self.screens = {'change_painting': self.delete_change_painting,
                        'lookup_painting': self.delete_lookup_painting,
                        'lookup_rack': self.delete_lookup_rack,
                        'scan_rack': self.delete_scan_rack,
                        'add_painting': self.delete_add_painting}

        self.image = None
        self.objectID = ''
        self.selectedObjectID = ''

        # Initialize Lookup and Sheet objects for object lookup and Google Sheet interfacing
        self.lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')
        self.sheet = Sheet('1N20NKyWzmx5AJJz9GlGuv7SC3nnVW5l3hkYDFsWdXx0', 'TMS Changes!A1:C', 'History Logger!A1:C')
        self.width = width
        self.height = height

        # Setup the frame
        self.parent = parent
        self.mainMenu = tk.Frame(master=self.parent)
        self.mainMenu.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu.pack(fill=tk.BOTH, expand=1) # Expand the frame to fill the root window


        self.show() # Render the items onto the frame

    def show(self):
        '''
        Adds elements to the mainMenu screen and renders the main menu

        :return: returns nothing
        '''
        # Setup font configurations
        s = ttk.Style()
        fontSize = int(0.024 * self.width)
        padding = int(0.015*self.width)
        s.configure('TButton', font=('arial', fontSize), padding=padding)
        s.configure('TLabel', font=('arial', fontSize))
        s.configure('TEntry', font=('arial', fontSize))

        # Create main menu buttons
        button1 = ttk.Button(self.mainMenu, text='Change a Painting\'s Location', command=self.change_painting)
        button2 = ttk.Button(self.mainMenu, text='Lookup a Painting', command=self.lookup_painting)
        button3 = ttk.Button(self.mainMenu, text='Lookup a Rack', command=self.lookup_rack)
        button4 = ttk.Button(self.mainMenu, text='Scan a Rack', command=self.scan_rack)
        button5 = ttk.Button(self.mainMenu, text='Add a Painting', command=self.add_painting)

        # Add buttons to the main menu screen
        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0)
        button3.grid(row=2, column=0)
        button4.grid(row=3, column=0)
        button5.grid(row=4, column=0)

        # Make column width take up the whole frame, and distribute each row evenly
        self.mainMenu.grid_columnconfigure(0, weight=1)
        self.mainMenu.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)

        self.mainMenu.lift() # bring the main menu screen to the front of the GUI

    def refresh_screens(self):
        '''
        Rendering method that unrenders the previous screen

        :return: returns nothing
        '''
        # Checks the unrender function name for each screen, and unrenders the screen it if it was the previous screen
        for function in self.screens:
            if function == self.screen:
                self.screens[function]()

    def change_painting(self):
        '''
        Shows the camera stream and updates the rest of the screens if the user wants to change the location of a painting

        :return: returns nothing
        '''
        # Unrender the previous screen
        self.refresh_screens()
        self.screen = 'change_painting'

        # Update the rest of the screens to change the location of a painting
        self.success = success.Success(self.parent, self.mainMenu, self)
        self.location = location.Location(self.parent, self.mainMenu, self,
                                          success=self.success,
                                          painting=self.selectedObjectID,
                                          lookup=self.lookup,
                                          sheet=self.sheet,
                                          width=self.width)
        self.entry = entry.Entry(self.parent, self.mainMenu, self, self.width)

        self.capture_image() # starts the camera stream to take a picture

    def delete_change_painting(self):
        '''
        Rendering method that deletes all the screens created by the user changing the location of a painting

        :return: returns nothing
        '''
        self.success.destroy()
        self.location.destroy()
        self.selection.destroy()
        self.entry.destroy()
        self.verification.destroy()

    def lookup_painting(self):
        '''
        Updates the rest of the screens if the user wants to lookup the location of a painting

        :return: returns nothing
        '''
        # Unrender the previous screen
        self.refresh_screens()
        self.screen = 'lookup_painting'

        # Update the rest of the screens to lookup the location of a painting
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, location='1A', objectID='2016.1.1')
        self.entry = entry.Entry(self.parent, self.mainMenu, self, self.width, selection=self.selection)

        self.entry.show() # renders the entry screen for the user to enter a object number

    def delete_lookup_painting(self):
        '''
        Rendering method that deletes all the screens created by the user looking up the location of a painting

        :return: returns nothing
        '''
        self.entry.destroy()
        self.selection.destroy()

    def lookup_rack(self):
        '''
        Updates the rest of the screens if the user wants to lookup paintings on a rack

        :return: returns nothing
        '''
        # Unrender the previous screen
        self.refresh_screens()
        self.screen = 'lookup_rack'
        
        # Update the rest of the screens to lookup the paintings on a rack
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, location='1A', objectID='2016.1.1')
        self.location = location.Location(self.parent, self.mainMenu, self,
                                          lookup=self.lookup,
                                          width=self.width,
                                          selection=self.selection)

        self.location.show() # Renders the rack entry screen for the user to enter a rack ID

    def delete_lookup_rack(self):
        '''
        Rendering method that deletes all the screens created by the user looking up the paintings on a rack

        :return: returns nothing
        '''
        self.selection.destroy()
        self.location.destroy()

    def scan_rack(self):
        '''
        Updates the rest of the screens if the user wants to scan the paintings on a rack

        :return: returns nothing
        '''
        # Unrender the previous screen
        self.refresh_screens()
        self.screen = 'scan_rack'

        # Update the rest of the screens to scan the paintings on a rack
        self.soon = comingSoon.ComingSoon(self.parent, self.mainMenu, self)

        self.soon.show() # Renders the coming soon screen

    def delete_scan_rack(self):
        '''
        Rendering method that deletes all the screens created by the user scanning the paintings on a rack

        :return: returns nothing
        '''
        self.soon.destroy()

    def add_painting(self):
        '''
        Updates the rest of the screens if the user wants to add a painting to the database

        :return: returns nothing
        '''
        # Unrender the previous screen
        self.refresh_screens()
        self.screen = 'add_painting'

        # Update the rest of the screens to add a painting to the database
        self.soon = comingSoon.ComingSoon(self.parent, self.mainMenu, self)

        self.soon.show() # Renders the coming soon screen

    def delete_add_painting(self):
        '''
        Rendering method that deletes all the screens created by the user adding a painting to the database

        :return: returns nothing
        '''
        self.soon.destroy()

    def capture_image(self):
        '''
        Start the camera, takes a picture, performs optical character recognition on the image, and shows the next screen

        :return: returns nothing
        '''
        cam = camera_ocr.CamOCR() # Initialize the camera
        self.objectID = cam.run() # Start the camera and get the object ID out of the image of the painting's tag

        # Update the rest of the screens to reflect the new object ID
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, location=self.location, objectID=self.objectID)
        self.verification = verification.Verification(self.parent, self.mainMenu, self, self.entry, self.selection, self.objectID)
        self.verification.show() # show the verification screen to make sure the number is correct

    def correct_objectID(self, objectID):
        '''
        Updates the Selection screen with a given object number to allow the user to select the correct painting

        :param objectID: a string describing the object number to update the Selection screen with
        :return: returns nothing
        '''
        self.objectID = objectID

        # Update the Selection screen and show it
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, location=self.location, objectID=self.objectID)
        self.selection.show()

    def select(self, selectedObjectID):
        '''
        Updates the Location screen with a given object number to allow the user to change the painting's location/rack

        :param selectedObjectID: a string describing the selected object number to update the Location screen with
        :return: returns nothing
        '''
        self.selectedObjectID = selectedObjectID

        # Update the Location screen and show it
        self.location = location.Location(self.parent, self.mainMenu, self, self.success, self.selectedObjectID, self.lookup, self.sheet, self.width)
        self.location.show()

    def searchRackNumber(self, rackInfo):
        '''
        Updates the Selection screen with given paintings to allow the user to view the paintings on a rack

        :param rackInfo: an array of dictionaries describing the paintings on a certain rack
        :return: returns nothing
        '''
        # Update the Selection screen with the given painting information, hide the location/rack entry screen, and show the Selection screen
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, rackPaintings=rackInfo)
        self.location.hide()
        self.selection.show()

    def searchObjectNumber(self, objectID):
        '''
        Updates the Selection screen with a given object number to allow the user to view search results of an object number

        :param objectID: a string describing the selected object number to update the Selection screen with
        :return: returns nothing
        '''
        # Update the Selection screen with the given object ID, hide the object ID entry screen, and show the Selection screen
        self.selection = selection.Selection(self.parent, self.mainMenu, self, self.lookup, self.width, objectID=objectID)
        self.entry.hide()
        self.selection.show()