import tkinter as tk

root = tk.Tk()

content = tk.Frame(root)
frame = tk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
namelbl = tk.Label(content, text="Name")
name = tk.Entry(content)

onevar = tk.BooleanVar(value=True)
twovar = tk.BooleanVar(value=False)
threevar = tk.BooleanVar(value=True)

one = tk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = tk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = tk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = tk.Button(content, text="Okay")
cancel = tk.Button(content, text="Cancel")

content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=3, rowspan=2)
namelbl.grid(column=3, row=0, columnspan=2)
name.grid(column=3, row=1, columnspan=2)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.mainloop()