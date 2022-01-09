import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview, Scrollbar


class Window:

    def __init__(self):
        self.init_window_db('CnkDatabase/chinook.db')  # DB connection
        self.all_tbls = []
        self.init_root()  # Root / Window creation
        self.init_first_line()
        # self.init_topframe()  # Top frame - Contains comboboxes, buttons and visual text
        # self.init_treeview()  # Bottom frame - Contains the treeview
        #
        # self.main_cmbx.bind("<<ComboboxSelected>>", self.first_choice)
        # self.add_cmbx.bind("<<ComboboxSelected>>", self.add_from_cmbx)
        #
        self.root.mainloop()  # Infinite run the program

    def init_window_db(self, pth):
        """
        Creates all db's vars
        :param pth: DB's path
        :return:    None
        """
        # self.crs = semQueries.db_connector(pth)  # Pointer to DB
        # self.all_tbls = semQueries.tables_names(self.crs)  # All tables' names
        # self.relations = semQueries.create_tbls_relations(self.crs, self.all_tbls)  # Relations between tables (dict)
        # self.tbls_cols = semQueries.tbls_dict(self.crs, self.all_tbls)  # Tables with their columns (dict)
        self.current_tbls = []  # Holds all current queries' tables
        self.all_related = []  # Holds all related tables to current tables

    def init_root(self):
        """
        Creates root
        :return: None
        """
        self.root = Tk()
        self.root.title('ChinookDB JOIN Queries')       # Window title
        self.root.geometry('1000x600')                  # Window size
        self.root.wm_minsize(width=900, height=550)     # Window MIN size
        self.root.wm_attributes("-topmost", 1)
        self.topFrame = Frame(self.root, background="skyblue")

    def init_combo_frame(self):
        self.frm_combos = Frame(self.topFrame)
        self.frm_combos.pack()
        self.frm_combos.grid(sticky=NW, ipadx=20)

    def init_first_line(self):

        Button(self.topFrame, text="This is ").grid(row=4, column=0, pady=8)
        Button(self.topFrame, text="another line").grid(row=5, column=0, sticky='ew')
        self.topFrame.pack()
        self.topFrame.grid(sticky=N, ipadx=20)

        self.init_main_combobox()
        self.init_extra_tables()


    def init_topframe(self):
        # Top frame - Will contain combobox, buttons and presents the list of the current tables.
        self.topFrame = Frame(self.root)  # Top frame
        self.topFrame.pack(pady=20)
        self.init_main_combobox()  # Add Combobox of all tables
        self.init_extra_tables()  # Add Combobox and buttons

        # Presents the query (lbl will be added)
        # self.frm_query, self.txt_query, self.scb_query = create_text(self.topFrame, "Query will be presented here")
        self.frm_query.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Joined tables text
        # self.tbls_join_txt, self.lbl_tbls_join = create_txt_lbl(
        #     self.topFrame, 'Joined Tables will be here', hig=8, wid=50)
        self.lbl_tbls_join.grid(row=2, column=3, columnspan=2, sticky="w", padx=10, pady=10)

        # Statistics
        # self.stat_txt, self.stat_lbl = create_txt_lbl(
        #     self.topFrame, 'Number of Columns: 0 Number of Rows: 0', wrpln=100, wid=60, hig=2, anc="nw")
        # self.stat_lbl.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=10)

    def init_main_combobox(self):
        self.lbl_main_table = Label(self.topFrame, text="First Table:", height=2, width=10, justify='left', background='pink')
        self.frm_main_cmbx = Frame(self.topFrame)
        self.main_cmbx = Combobox(self.frm_main_cmbx, values=self.all_tbls, width=20)
        self.lbl_main_table.grid(row=0, column=0, sticky=W)  # Location
        self.frm_main_cmbx.grid(row=1, column=0, pady=10)  # Location
        self.main_cmbx.pack()

    def init_extra_tables(self):
        """
        Init window features for adding another table(s) / removing table(s)
        :return: None
        """
        # Combobox
        self.lbl_add_tbls = Label(self.topFrame, text="Add Table:", height=2, width=10, justify='left', background='pink')
        self.frm_add_cmbx = Frame(self.topFrame)
        self.add_cmbx = Combobox(self.frm_add_cmbx, values=self.all_related, width=20)
        self.lbl_add_tbls.grid(row=2, column=0)  # Location
        self.frm_add_cmbx.grid(row=3, column=0)  # Location
        self.add_cmbx.pack()

        # Buttons
        # self.frm_btns = Frame(self.topFrame)
        # self.frm_btns.grid(row=0, column=4)
        # self.undo_btn = Button(self.frm_btns, text="Undo", width=10, command=self.cmnd_undo)  # Undo button
        # self.reset_btn = Button(self.frm_btns, text="Reset", width=10, command=self.cmnd_reset)  # Reset button
        # self.undo_btn.pack(side='left')
        # self.reset_btn.pack(side='right')

    def init_treeview(self):
        self.frm_trv = Frame(self.root)
        self.frm_trv.pack(side='bottom', padx=20, pady=10, fill='both', expand=True)
        self.trv = Treeview(self.frm_trv, height=25, show='headings')  # Treeview
        vsb = ttk.Scrollbar(self.frm_trv, orient="vertical", command=self.trv.yview)  # Treeview vertical scrollbar
        hsb = ttk.Scrollbar(self.frm_trv, orient="horizontal", command=self.trv.xview)  # Treeview horizontal scrollbar
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.trv.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        self.trv.pack(fill='both', expand=True)

    def first_choice(self, event):
        self.current_tbls = []
        self.add_from_cmbx(event)

    def add_from_cmbx(self, event):
        self.current_tbls.append(event.widget.get())
        self.add_cmbx.set('')
        self.update_query()

    def cmnd_undo(self):
        if self.current_tbls:
            self.current_tbls.pop()
        if not self.current_tbls:
            self.cmnd_reset()
        else:
            self.add_cmbx.set('')
            self.update_query()

    def cmnd_reset(self):
        self.current_tbls = []
        self.main_cmbx.set('')
        self.tbls_join_txt.set('No tables!')
        self.update_query()

    def remove_last_table(self):
        if self.current_tbls:
            self.current_tbls.pop()
        self.update_query()

    def update_query(self):
        self.txt_query.delete('1.0', 'end')
        if self.current_tbls:
            qry = semQueries.query_creation(self.current_tbls, len(self.current_tbls),
                                            self.relations, self.tbls_join_txt)
            qry_str = query_format(qry)
            print(qry_str)
            self.txt_query.insert('0.0', qry_str)
            self.stat_txt.set(data(self.crs, qry_str, self.trv, self.current_tbls, self.tbls_cols))
        else:
            self.txt_query.insert('1.0', "No tables were chosen")
            self.trv.delete(*self.trv.get_children())
        self.all_related = semQueries.get_all_related(self.current_tbls, self.relations)
        self.add_cmbx['values'] = self.all_related


wind = Window()