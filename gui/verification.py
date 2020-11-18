#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk
from tkinter import ttk
import cv2


class Verification:
    '''
    Contains functions to create the object ID Verification screen of the GUI,
    and link the object ID Verification screen to the main menu of the GUI
    '''
    def __init__(self, parent, menu, mainMenu, entryPage, selectionPage, objectID):
        '''
        Creates the object ID Verification screen of the GUI

        :param parent: the tkinter Frame that is the container for every page
        :param menu: the tkinter Frame of the main menu
        :param mainMenu: the mainMenu object that links together all screens
        :param entryPage: the object ID entry page to proceed to if the number is wrong
        :param selectionPage: the painting selection page to proceed to if the number is correct
        :param objectID: the object ID to display and verify its accuracy
        :return: returns nothing
        '''
        self.verification = tk.Frame(master=parent)
        self.verification.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
        self.mainMenu = mainMenu
        self.menu = menu
        self.entryPage = entryPage
        self.selectionPage = selectionPage
        self.parent = parent

        # Add restart button to top left
        restart = ttk.Button(self.verification, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, columnspan=2, sticky='w')

        # Add title text
        title = ttk.Label(self.verification, text='Verify OCR Value')
        title.grid(row=1, column=0, columnspan=2)

        # Add verification prompt message
        prompt = ttk.Label(self.verification, text='Is the object number correct?')
        prompt.grid(row=2, column=0, columnspan=2)

        # Display the object ID to verify
        number = ttk.Label(self.verification, text=objectID, style='TLabel')
        number.grid(row=3, column=0, columnspan=2)

        # Add buttons to allow user to select whether the object ID is correct or not
        wrong = ttk.Button(self.verification, text='No', command=self.entryPage.show)
        correct = ttk.Button(self.verification, text='Yes', command=self.selectionPage.show)
        wrong.grid(row=4, column=0)
        correct.grid(row=4, column=1)

        # Set the row and column spacing
        self.verification.grid_columnconfigure([0, 1], weight=1)
        self.verification.grid_rowconfigure([1, 2, 3, 4], weight=1)

    def show(self):
        '''
        Place the Verification frame in the parent Frame and bring it to the front to show it

        :return: returns nothing
        '''
        self.verification.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.verification.lift()
        cv2.destroyAllWindows() # closes any camera windows

    def hide(self):
        '''
        Remove the Verification frame from the parent Frame and bring the main menu to the front to show it

        :return: returns nothing
        '''
        self.verification.pack_forget()
        self.menu.lift()

    def destroy(self):
        '''
        Unrender the Verification screen

        :return: returns nothing
        '''
        self.verification.destroy()