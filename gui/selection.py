#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Selection:
    '''
    Contains functions to create the painting Selection screen of the GUI,
    and link the painting Selection screen to the main menu of the GUI
    '''
    def __init__(self, parent, menu, mainMenu, lookup, width, location=None, objectID=None, rackPaintings=None, entryPage=None):
        '''
        Creates the painting Selection screen of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :param menu: the tkinter Frame of the main menu
        :param mainMenu: the mainMenu object that links together all screens
        :param lookup: the Lookup object to allow object/rack lookup
        :param width: the width of the screen
        :param location: the Location/rack entry screen (if changing the location of a painting)
        :param objectID: the object ID to lookup in the database
        :param rackPaintings: the paintings on a given rack (if looking up the paintings on a certain rack)
        :param entryPage: the entry page to go to if the user wants to manually enter the painting object ID
        :return: returns nothing
        '''
        self.lookup = lookup
        self.selection = tk.Frame(master=parent)
        self.selection.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu = mainMenu
        self.menu = menu
        self.location = location
        self.parent = parent
        self.entryPage = entryPage

        # Add restart button to top left
        restart = ttk.Button(self.selection, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        # Render the correct title and render the correct buttons with the correct functions for the correct action
        if rackPaintings == None and location != None and objectID != None and entryPage != None:
            # If we're changing the location of a painting and have just exited the camera

            # Render the correct title for the action
            title = ttk.Label(self.selection, text='Select the correct painting')
            title.grid(row=1, column=0, columnspan=2)

            # Create and render the selection box with a scrollbar
            self.options = tk.Listbox(self.selection, height=int(0.015 * width), font=tkFont.Font(size=int(0.0165 * width)))
            self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
            self.options.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.options.yview)

            c = 1
            # Add the paintings to the selection box
            if self.lookup.object_exists(objectID, decimals=False):
                self.paintings = self.lookup.get_info(objectID, decimals=False)
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
                # If no paintings in the database were found
                self.options.insert(c, f'Found no results for object number {objectID}')
            
            # Create and render manual entry button
            entry = ttk.Button(self.selection, text='Manual Entry', command=self.entryPage.show)
            entry.grid(row=3, column=0, sticky='w')
        elif rackPaintings == None and location != None and objectID != None and entryPage == None:
            # If we're changing the location of a painting and have correct the object ID number

            # Render the correct title for the action
            title = ttk.Label(self.selection, text='Select the correct painting')
            title.grid(row=1, column=0, columnspan=2)

            # Create and render the selection box with a scrollbar
            self.options = tk.Listbox(self.selection, height=int(0.015 * width), font=tkFont.Font(size=int(0.0165 * width)))
            self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
            self.options.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.options.yview)

            c = 1
            # Add the paintings to the selection box
            if self.lookup.object_exists(objectID, decimals=False):
                self.paintings = self.lookup.get_info(objectID, decimals=False)
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
                # If no paintings in the database were found
                self.options.insert(c, f'Found no results for object number {objectID}')
        elif rackPaintings != None and location == None and objectID == None:
            # If we're looking up paintings on a rack (using Rack Lookup feature)

            # Render the correct title for the action
            title = ttk.Label(self.selection, text='Rack Search Results')
            title.grid(row=1, column=0, columnspan=2)

            # Create and render the selection box with a scrollbar
            self.options = tk.Listbox(self.selection, height=int(0.015 * width), font=tkFont.Font(size=int(0.0165 * width)))
            self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
            self.options.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.options.yview)

            c = 1
            # Add the paintings to the selection box
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
                # If no paintings were found on that rack
                self.options.insert(c, f'Found no results for that rack number')
        elif rackPaintings == None and location == None and objectID != None:
            # If we're looking up paintings based on an object ID number (using Painting Lookup feature)

            # Render the correct title for the action
            title = ttk.Label(self.selection, text='Painting Search Results')
            title.grid(row=1, column=0, columnspan=2)

            # Create and render the selection box with a scrollbar
            self.options = tk.Listbox(self.selection, height=int(0.015 * width), font=tkFont.Font(size=int(0.0165 * width)))
            self.scrollbar = tk.Scrollbar(self.selection, orient=tk.VERTICAL)
            self.options.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.options.yview)

            c = 1
            # Add the paintings to the selection box
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
                # If no paintings were found with that object ID
                self.options.insert(c, f'Found no results for object number {objectID}')

        # Render the selection box and scrollbar
        self.options.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.scrollbar.grid(row=2, column=1, sticky='nse')

        # Create and render the scroll up and scroll down buttons
        up = ttk.Button(self.selection, text='Scroll up', command=lambda: self.options.yview_scroll(-1, tk.PAGES))
        up.grid(row=1, column=1, sticky='se')
        down = ttk.Button(self.selection, text='Scroll down', command=lambda: self.options.yview_scroll(1, tk.PAGES))
        down.grid(row=3, column=1, sticky='ne')

        # Set row and column spacing
        self.selection.grid_columnconfigure(0, weight=1)
        self.selection.grid_rowconfigure([1, 3], weight=1)

    def select(self):
        '''
        Processes a user clicking on a certain painting and passes it onto the rack entry screen (if changing the location of a painting)

        :return: returns nothing
        '''
        selectedLine = self.options.curselection()[0] # get the painting the user selected
        selectedID = self.paintings[selectedLine] # get the information for the painting the user selected
        self.mainMenu.select(selectedID) # pass the selected painting onto the Location/rack entry screen to change its location

    def show(self):
        '''
        Place the Selection frame in the parent Frame and bring it to the front to show it

        :return: returns nothing
        '''
        self.selection.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.selection.lift()

    def hide(self):
        '''
        Remove the Selection frame from the parent Frame and bring the main menu to the front to show it

        :return: returns nothing
        '''
        self.selection.pack_forget()
        self.menu.lift()
    
    def destroy(self):
        '''
        Unrender the Selection screen

        :return: returns nothing
        '''
        self.selection.destroy()