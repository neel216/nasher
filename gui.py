#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk
from gui import mainMenu


window = tk.Tk() # Create the Tkinter window
window.title('Nasher Database System')
width  = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f'{width}x{height - 60}+0+0') # Position window in top left of screen and set the dimensions to be full screen
window.resizable(0, 0) # Don't allow resizing in the x or y direction

root = tk.Frame(master=window) # Create the master frame
root.pack_propagate(0) # Don't allow the frames inside to determine the master frame's width/height
root.pack(fill=tk.BOTH, expand=1) # Expand the master frame to fill the root window

gui = mainMenu.MainMenu(root, width, height) # Start the main menu

window.mainloop() # Start the event listener