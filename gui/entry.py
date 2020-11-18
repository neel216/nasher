#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Entry:
    '''
    Contains functions to create the Entry/painting ID entry screen of the GUI,
    and link the Entry/painting ID entry screen to the main menu of the GUI
    '''
    def __init__(self, parent, menu, mainMenu, width, selection=None):
        '''
        Creates the Entry/painting ID entry screen of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :param menu: the tkinter Frame of the main menu
        :param mainMenu: the mainMenu object that links together all screens
        :param width: the width of the screen
        :param selection: the Selection screen to allow the user to choose between multiple paintings
        :return: returns nothing
        '''
        self.entry = tk.Frame(master=parent)
        self.entry.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu = mainMenu
        self.menu = menu
        self.parent = parent

        # Add restart button to top left
        restart = ttk.Button(self.entry, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        # Render the correct title and link the correct function to the 'Ok' button to reflect the correct action
        if not selection:
            # If we are changing the location of a painting
            title = ttk.Label(self.entry, text='Enter the correct object number')
            title.grid(row=1, column=0, columnspan=3)

            # Setup the text entry box
            self.object_id = tk.StringVar()
            self.entryBox = ttk.Entry(self.entry, textvariable=self.object_id, font=tkFont.Font(size=int(0.024 * width)))
            self.entryBox.grid(row=2, column=0, columnspan=3)

            self.entryKeyboard() # Render the keyboard

            ok = ttk.Button(self.entry, text='Ok', command=self.correct_object_id)
            ok.grid(row=7, column=2, columnspan=3)
        else:
            # If we are looking up the location of a painting
            title = ttk.Label(self.entry, text='Enter the object number')
            title.grid(row=1, column=0, columnspan=3)

            # Setup the text entry box
            self.object_id = tk.StringVar()
            self.entryBox = ttk.Entry(self.entry, textvariable=self.object_id, font=tkFont.Font(size=int(0.024 * width)))
            self.entryBox.grid(row=2, column=0, columnspan=3)

            self.entryKeyboard() # Render the keyboard

            ok = ttk.Button(self.entry, text='Ok', command=self.search_object_id)
            ok.grid(row=7, column=2, columnspan=3)

        # Set row and column spacing
        self.entry.grid_columnconfigure([0, 1, 2], weight=1)
        self.entry.grid_rowconfigure([1, 2, 7], weight=1)
        self.entry.grid_rowconfigure([3, 4, 5, 6], weight=1)

    def appendChar(self, char):
        '''
        Enters a character into the text entry box

        :param char: the character to enter
        :return: returns nothing
        '''
        i = len(self.object_id.get())
        self.entryBox.insert(i, char)
    
    def deleteChar(self):
        '''
        Deletes a character from the text entry box

        :return: returns nothing
        '''
        i = len(self.object_id.get()) - 1
        self.entryBox.delete(i)

    def entryKeyboard(self):
        '''
        Creates and renders the keyboard to enter a painting ID

        :return: returns nothing
        '''
        # Create buttons for the keyboard
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

        # Render each button
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
        '''
        Takes the information from the painting ID entry text box and updates the Selection screen with all paintings containing the given number.
        Used during the Changing the Location of a Painting function.

        :return: returns nothing
        '''
        self.mainMenu.correct_objectID(self.object_id.get())
        self.object_id.set('') # clears text entry box
    
    def search_object_id(self):
        '''
        Takes the information from the painting ID entry text box and searches the database for all paintings containing that number.
        Used during the Lookup a Painting function.

        :return: returns nothing
        '''
        self.mainMenu.searchObjectNumber(self.object_id.get())
        self.object_id.set('') # clears text entry box
    
    def show(self):
        '''
        Place the Entry frame in the parent Frame and bring it to the front to show it

        :return: returns nothing
        '''
        self.entry.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.entry.lift()

    def hide(self):
        '''
        Remove the Entry frame from the parent Frame and bring the main menu to the front to show it

        :return: returns nothing
        '''
        self.entry.place_forget()
        self.menu.lift()
    
    def destroy(self):
        '''
        Unrender the Entry screen

        :return: returns nothing
        '''
        self.entry.destroy()