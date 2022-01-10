import tkinter
from tkinter import *
from tkinter import ttk
#
root = Tk()
root.geometry('1050x600')  # Window size
# root.wm_minsize(width=1150, height=550)  # Window MIN size
# root.wm_attributes("-topmost", 1)
# #
# # canvas = Canvas(frame, bg='white', width=300, height=300,
# #                 scrollregion=(0, 0, 500, 500))
# #
# # hbar = Scrollbar(frame, orient=HORIZONTAL)
# # hbar.pack(side=BOTTOM, fill=X)
# # hbar.config(command=canvas.xview)
# #
# # vbar = Scrollbar(frame, orient=VERTICAL)
# # vbar.pack(side=RIGHT, fill=Y)
# # vbar.config(command=canvas.yview)
# #
# # canvas.config(width=300, height=300)
# # canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
# # canvas.pack(side=LEFT, expand=True, fill=BOTH)
# #
frm1 = Frame(root, bg='red', width=200, height=200, pady=1)
frm2 = Frame(root, bg='pink', width=600, height=10, padx=1, pady=1)
frm3 = Frame(root, bg='yellow', width=200, height=90, pady=1)
frm4 = Frame(root, bg='blue', width=600, height=140, padx=1, pady=1)
frm5 = Frame(root, bg='green', width=800, height=200, padx=1, pady=1)
# frm6 = Frame(frame, bg='orange')

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

frm1.grid(row=0, sticky='nw', padx=20, pady=20)
frm2.grid(row=0, column=1, sticky='n',padx=10, pady=20)
frm3.grid(row=2, column=0, rowspan=3)
frm4.grid(row=1, column=1, rowspan=4, columnspan=3)
frm5.grid(row=4, column=0, rowspan=4, columnspan=5)
#
# # frm1.pack(expand=True, fill=BOTH)
# # frm2.pack(expand=True, fill=BOTH)
# # frm3.pack(expand=True, fill=BOTH)
# # frm4.pack(expand=True, fill=BOTH)
# # frm5.pack(expand=True, fill=BOTH)

#
# root = Tk()
# root.title('Model Definition')
# root.geometry('{}x{}'.format(460, 350))
#
# # create all of the main containers
# top_frame = Frame(root, bg='cyan', width=450, height=50, pady=3)
# center = Frame(root, bg='gray', width=50, height=40, padx=3, pady=3)
# btm_frame = Frame(root, bg='pink', width=450, height=45, pady=3)
# # btm_frame2 = Frame(root, bg='lavender', width=450, height=60, pady=3)
#
# # layout all of the main containers
# root.grid_rowconfigure(1, weight=1)
# root.grid_columnconfigure(0, weight=1)
#
# top_frame.grid(row=0, sticky="ew")
# center.grid(row=1, sticky="nsew")
# btm_frame.grid(row=3, sticky="ew")
# # btm_frame2.grid(row=4, sticky="ew")
#
# # create the widgets for the top frame
# model_label = Label(top_frame, text='Model Dimensions')
# width_label = Label(top_frame, text='Width:')
# length_label = Label(top_frame, text='Length:')
# entry_W = Entry(top_frame, background="pink")
# entry_L = Entry(top_frame, background="orange")
#
# # layout the widgets in the top frame
# model_label.grid(row=0, columnspan=3)
# width_label.grid(row=1, column=0)
# length_label.grid(row=1, column=2)
# entry_W.grid(row=1, column=1)
# entry_L.grid(row=1, column=3)
#
# # create the center widgets
# center.grid_rowconfigure(0, weight=1)
# center.grid_columnconfigure(1, weight=1)
# #
# ctr_left = Frame(center, bg='blue', width=100, height=190)
# ctr_mid = Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3)
# ctr_right = Frame(center, bg='green', width=100, height=190, padx=3, pady=3)
#
# ctr_left.grid(row=0, column=0, sticky="ns")
# ctr_mid.grid(row=0, column=1, sticky="nsew")
# ctr_right.grid(row=0, column=2, sticky="ns")

root.mainloop()