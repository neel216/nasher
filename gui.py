import tkinter as tk
from gui import mainMenu


window = tk.Tk()
window.title('Nasher Database System')
width  = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f'{width}x{height - 60}+0+0')
window.resizable(0, 0) # Don't allow resizing in the x or y direction

root = tk.Frame(master=window)
root.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
root.pack(fill=tk.BOTH, expand=1) # Expand the frame to fill the root window

gui = mainMenu.MainMenu(root)

window.mainloop()