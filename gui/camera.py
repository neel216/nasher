import tkinter as tk
from tkinter import ttk

class Camera:
    def __init__(self, parent, menu, mainMenu, nextPage):
        self.camera = tk.Frame(master=parent)
        self.camera.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.mainMenu = mainMenu
        self.nextPage = nextPage
        self.menu = menu
        self.parent = parent

        restart = ttk.Button(self.camera, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        self.lmain = tk.Label(self.camera)
        self.lmain.grid(row=1, column=0)

        takePicture = ttk.Button(self.camera, text='Open Camera', command=self.mainMenu.capture_image)
        takePicture.grid(row=2, column=0)

        self.camera.grid_columnconfigure(0, weight=1)
        self.camera.grid_rowconfigure(2, weight=1)

    def show(self):
        self.camera.place(in_=self.parent, x=0, y=0, relwidth=1, relheight=1)
        self.camera.lift()

    def hide(self):
        self.camera.place_forget()
        self.menu.lift()

    def destroy(self):
        self.camera.destroy()