#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk
from tkinter import ttk


class ComingSoon:
    '''
    Contains functions to create the Coming Soon screen of the GUI,
    and link the Coming Soon screen to the main menu of the GUI
    '''
    def __init__(self, parent, menu, mainMenu):
        '''
        Creates the Coming Soon screen of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :param menu: the tkinter Frame of the main menu
        :param mainMenu: the mainMenu object that links together all screens
        :return: returns nothing
        '''
        self.soon = tk.Frame(master=parent)
        self.soon.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu = mainMenu
        self.menu = menu
        self.parent = parent

        # Add the Coming Soon text to the screen and render it
        title = ttk.Label(self.soon, text='Feature Coming Soon!')
        title.grid(row=0, column=0)

        # Add restart button to top left
        restart = ttk.Button(self.soon, text='Restart', command=self.hide)
        restart.grid(row=2, column=0)

        # Set the row and column spacing
        self.soon.grid_columnconfigure(0, weight=1)
        self.soon.grid_rowconfigure([0, 1, 2], weight=1)

    def show(self):
        '''
        Place the Coming Soon frame in the parent Frame and bring it to the front to show it

        :return: returns nothing
        '''
        self.soon.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.soon.lift()

    def hide(self):
        '''
        Remove the Coming Soon frame from the parent Frame and bring the main menu to the front to show it

        :return: returns nothing
        '''
        self.soon.pack_forget()
        self.menu.lift()
    
    def destroy(self):
        '''
        Unrender the Coming Soon screen

        :return: returns nothing
        '''
        self.soon.destroy()