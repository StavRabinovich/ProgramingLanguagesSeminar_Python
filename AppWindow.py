from tkinter import *
from tkinter import ttk
import sqlite3

window = Tk()
frm = ttk.Frame(window, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=window.destroy).grid(column=1, row=0)
entry = ttk.Entry().grid(column=2, row=3)

lbl = ttk.Label(master=frm, text="f").grid(column=3, row=3)
ttk.Label.config

window.mainloop()

# window = Tk()
# window.geometry("800x600") # Window size
# window.title("Header Title") # Header
# lbl = ttk.Label(window, text = "Label 1", font=("Tahoma Bold", 24)).pack()
# # lbl.grid(column=1, row=2)
# btn = Button (window, text="Enter").pack()
# # bt.grid(column=2, row=2)
# # fg text color;  bg bg color
#
# def clicked1(): # ?
#     ttk.Label.configure(lbl, text="btn was clicked!")
#
#
# btn = Button(window, text="Enter", command = clicked1).pack()
# txt = Entry(window, width=10).pack()
#
# def clicked2():
#     res = "Welcome! to " # + lbl.get()
#     lbl = ttk.Label.configure(text=res)
#
# btn = Button (window, text="Enter", command = clicked2).pack()
#
#
# window.mainloop() # Will run the App window
