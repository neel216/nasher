#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Location:
    '''
    Contains functions to create the Location/rack entry screen of the GUI,
    and link the Location/rack entry screen to the main menu of the GUI
    '''
    def __init__(self, parent, menu, mainMenu, success=None, painting=None, lookup=None, sheet=None, width=None, selection=None):
        '''
        Creates the Location/rack entry screen of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :param menu: the tkinter Frame of the main menu
        :param mainMenu: the mainMenu object that links together all screens
        :param success: if the next screen is the Success screen (meaning we're changing the location of a painting)
        :param painting: the information of the painting to update (if we're changing the location of a painting)
        :param lookup: the Lookup object to allow object/rack lookup
        :param sheet: the Sheet object to update data in a Google Sheet
        :param width: the width of the screen
        :param selection: the Selection screen to allow the user to choose between multiple paintings
        :return: returns nothing
        '''
        self.location = tk.Frame(master=parent)
        self.location.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu = mainMenu
        self.menu = menu
        self.success = success
        self.painting = painting
        self.lookup = lookup
        self.sheet = sheet
        self.parent = parent
        self.selection = selection
        
        # Add restart button to top left
        restart = ttk.Button(self.location, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        # Change the title of the screen to reflect the correct action
        if success:
            title = ttk.Label(self.location, text='Enter the new rack')
        else:
            title = ttk.Label(self.location, text='Enter the rack')
        title.grid(row=1, column=0, columnspan=3)
        
        # Setup up textbox for input
        self.rack = tk.StringVar()
        self.entry = ttk.Entry(self.location, textvariable=self.rack, font=tkFont.Font(size=int(0.024 * width)))
        self.entry.grid(row=2, column=0, columnspan=3)

        self.selectionKeyboard() # render keyboard

        # Attach the correct function to the 'Ok' button to reflect the correct action
        if success:
            ok = ttk.Button(self.location, text='Ok', command=self.submitRack)
        else:
            ok = ttk.Button(self.location, text='Ok', command=self.searchRack)
        ok.grid(row=8, column=2, columnspan=3)

        # Configure row and column spacing
        self.location.grid_columnconfigure([0, 1, 2], weight=1)
        self.location.grid_rowconfigure([1, 2, 8], weight=1)
        self.location.grid_rowconfigure([3, 4, 5, 6, 7], weight=1)

    def appendChar(self, char):
        '''
        Process a character and enter it into the text entry if it is allowed to be entered

        :param char: the character entry to process
        :return: returns nothing
        '''
        if len(self.rack.get()) == 0 and char in 'AB':
            # Don't do anything if there are no characters and the user is trying to enter an A or B
            pass
        elif len(self.rack.get()) == 2 and self.rack.get()[-1] in 'AB':
            # Don't do anything if the text entry currently has a number and an A or B at the end
            pass
        elif len(self.rack.get()) == 2 and self.rack.get()[-1] not in 'AB' and char not in 'AB':
            # Don't do anything if the text entry has a 2 digit number and the user is trying to enter another number
            pass
        elif len(self.rack.get()) == 3:
            # Don't do anything if there are 3 character in the text entry
            pass
        else:
            # If none of the above conditions are true, allow the user to enter the character
            i = len(self.rack.get())
            self.entry.insert(i, char)
    
    def deleteChar(self):
        '''
        Deletes a character from the text entry box

        :return: returns nothing
        '''
        i = len(self.rack.get()) - 1
        self.entry.delete(i)

    def selectionKeyboard(self):
        '''
        Creates and renders the keyboard to enter a rack

        :return: returns nothing
        '''
        # Create buttons for the keyboard
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

        # Render each button
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
        zero.grid(row=7, column=1)
        delete.grid(row=7, column=2)

    def submitRack(self):
        '''
        Takes the information from the rack entry text box and changes the location of a given painting

        :return: returns nothing
        '''
        # Update the Google Sheet with the change for the registrar/TMS
        self.sheet.add_rows([[self.painting['objectID'], self.painting['artist'], self.painting['otherInfo'], self.painting['room'] + ', ' + self.painting['location'], 'Nasher Painting Storage Room' + ', ' + self.rack.get()]])

        # Update local data
        self.lookup.edit_location(self.painting['index'], 'Nasher Painting Storage Room', self.rack.get())

        # Show the Success screen
        self.success.show()
    
    def searchRack(self):
        '''
        Takes the information from the rack entry text box and searches the database for all paintings on the rack

        :return: returns nothing
        '''
        # Get the rack ID from the rack entry box
        rack = self.lookup.get_rack(self.rack.get())

        # Call the searchRackNumber() function to search all paintings in the database on the given rack and show the Selection screen
        self.mainMenu.searchRackNumber(rack)

    def show(self):
        '''
        Place the Location frame in the parent Frame and bring it to the front to show it

        :return: returns nothing
        '''
        self.location.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.location.lift()

    def hide(self):
        '''
        Remove the Location frame from the parent Frame and bring the main menu to the front to show it

        :return: returns nothing
        '''
        self.location.place_forget()
        self.menu.lift()

    def destroy(self):
        '''
        Unrender the Location screen

        :return: returns nothing
        '''
        self.location.destroy()