import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview, Scrollbar
import semQueries


def data(mycur, query, tree, current_tbls, table_columns):
    """
    Import data using query, and adding to the tree (sorted)
    :param mycur:           my cursor
    :param query:           (String) the query
    :param tree:            (treeview) UI of the query results
    :param current_tbls:    list of tables in current query
    :param table_columns:   (dict) tables and their cols' names
    :return:    (String) num of cols AND num of imported rows
    """
    for x in tree.get_children():
        tree.delete(x)

    query = query.replace('main.', '')
    print(query)

    q_data = mycur.execute(query)   # Query's data
    rows = mycur.fetchall()

    param = [i for i in range(1, len(q_data.description) + 1)]
    tree.configure(columns=param)

    count = 0
    for idx, col in enumerate(q_data.description):
        if count < len(table_columns[current_tbls[0]]):
            table_name = current_tbls[0]
        elif current_tbls[1] is not None and count < (
                len(table_columns[current_tbls[0]]) + len(table_columns[current_tbls[1]])):
            table_name = current_tbls[1]
        else:
            table_name = current_tbls[2]
        count += 1
        table_name = f'{col[0]}'
        tree.heading(idx + 1, text=table_name, anchor="w")
        tree.column(idx + 1, width=88, stretch=NO)

    for row in rows:
        tree.insert('', 'end', values=row)

    semQueries.sort_treeview_by_col(tree, 0, False)
    return f'Columns Count: {len(q_data.description)}\t\tRows Count: {len(rows)}'


def create_txt_lbl(frm, txt, wrpln=250, fnt="Segoe UI", fnt_sz=10, hig=5, anc="w", wid=30, jst='left', lbl_pack=False):
    my_txt = StringVar()
    my_txt.set(txt)
    lbl_txt = Label(frm, textvariable=my_txt, wraplength=wrpln, font=(fnt, fnt_sz),
                    height=hig, anchor=anc, width=wid, justify=jst)
    if lbl_pack:
        lbl_txt.pack()
    return my_txt, lbl_txt


class Window:

    def __init__(self):
        self.init_window_db('CnkDatabase/chinook.db')   # DB connection
        self.init_root()        # Root / Window creation
        self.init_topframe()    # Top frame - Contains coboboxes, buttons and visual text
        self.init_treeview()    # Bottom frame - Contains the treeview

        self.main_cmbx.bind("<<ComboboxSelected>>", self.first_choice)
        self.add_cmbx.bind("<<ComboboxSelected>>", self.add_from_cmbx)

        self.root.mainloop()  # Infinite run the program

    def init_window_db(self, pth):
        """
        Creates all db's vars
        :param pth: DB's path
        :return:    None
        """
        self.crs = semQueries.db_connector(pth)  # Pointer to DB
        self.all_tbls = semQueries.tables_names(self.crs)  # All tables' names
        self.relations = semQueries.create_tbls_relations(self.crs, self.all_tbls)  # Relations between tables (dict)
        self.tbls_cols = semQueries.tbls_dict(self.crs, self.all_tbls)  # Tables with their columns (dict)
        self.current_tbls = []  # Holds all current queries' tables
        self.all_related = []   # Holds all related tables to current tables

    def init_root(self):
        """
        Creates root
        :return: None
        """
        self.root = Tk()
        self.root.title('Seminar Project - Stav Suzan Rabinovich 208661090')  # Window title
        self.root.geometry('1000x600')  # Window size
        self.root.wm_attributes("-topmost", 1)  # ?

    def init_topframe(self):
        # Top frame - Will contain combobox, buttons and presents the list of the current tables.
        self.topFrame = Frame(self.root)    # Top frame
        self.topFrame.pack()
        self.init_main_combobox()           # Add Combobox of all tables
        self.init_extra_tables()            # Add Combobox and buttons

        # Presents the query (lbl will be added)
        self.frm_query = Frame(self.topFrame)
        self.frm_query.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.query_txt, self.lbl_query = create_txt_lbl(
            self.frm_query, "Query will be presented here", wid=60, lbl_pack=True)

        # Joined tables text
        self.tbls_join_txt, self.lbl_tbls_join = create_txt_lbl(
            self.topFrame, 'Joined Tables will be presented here', hig=8, wid=30)
        self.lbl_tbls_join.grid(row=2, column=3, sticky="w", padx=10, pady=10)

        # Joined columns text
        self.cols_join_txt, self.lbl_cols_join = create_txt_lbl(
            self.topFrame, 'Joined Columns will be presented here', hig=8, wid=35)
        self.lbl_cols_join.grid(row=2, column=4, sticky="w", padx=10, pady=10)

        # Statistics
        self.stat_txt, self.stat_lbl = create_txt_lbl(
            self.topFrame, 'Number of Columns: 0 Number of Rows: 0', wrpln=100, wid=20, hig=2, anc="nw")
        self.stat_lbl.grid(row=3, column=0, sticky='w', padx=10, pady=10)

    def init_main_combobox(self):
        self.lbl_main_table = Label(self.topFrame, text="First Table:", height=2, width=10, justify='left')
        self.frm_main_cmbx = Frame(self.topFrame)
        self.main_cmbx = Combobox(self.frm_main_cmbx, values=self.all_tbls, width=25)
        self.lbl_main_table.grid(row=0, column=0, pady=20)   # Location
        self.frm_main_cmbx.grid(row=0, column=1, pady=10)    # Location
        self.main_cmbx.pack()

    def init_extra_tables(self):
        """
        Init window features for adding another table(s) / removing table(s)
        :return: None
        """
        # Combobox
        self.lbl_add_tbls = Label(self.topFrame, text="Add Table:", height=2, width=10, justify='left')
        self.frm_add_cmbx = Frame(self.topFrame)
        self.add_cmbx = Combobox(self.frm_add_cmbx, values=self.all_related, width=25)
        self.lbl_add_tbls.grid(row=0, column=2)     # Location
        self.frm_add_cmbx.grid(row=0, column=3)     # Location
        self.add_cmbx.pack()

        # Buttons
        self.frm_btns = Frame(self.topFrame)
        self.frm_btns.grid(row=0, column=4)
        self.undo_btn = Button(self.frm_btns, text="Undo", width=10, command=self.cmnd_undo)        # Undo button
        self.reset_btn = Button(self.frm_btns, text="Reset", width=10, command=self.cmnd_reset)     # Reset button
        self.undo_btn.pack(side='left')
        self.reset_btn.pack(side='right')

    def init_treeview(self):
        self.frm_trv = Frame(self.root)
        self.frm_trv.pack(side='bottom', padx=20, pady=10, fill='both', expand=True)
        self.trv = Treeview(self.frm_trv, height=25, show='headings')                   # Treeview
        vsb = ttk.Scrollbar(self.frm_trv, orient="vertical", command=self.trv.yview)    # Treeview vertical scrollbar
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
        self.update_query()

    def cmnd_undo(self):
        self.current_tbls.pop()
        self.update_query()

    def cmnd_reset(self):
        self.current_tbls = []
        self.update_query()

    def remove_last_table(self):
        if self.current_tbls:
            self.current_tbls.pop()
        self.update_query()

    def update_query(self):
        if self.current_tbls:
            qry = semQueries.query_creation(self.current_tbls, len(self.current_tbls),
                                        self.relations, self.tbls_join_txt, self.cols_join_txt)
            qry_str = qry.split("FROM")[0] + '\nFROM' + qry.split("FROM")[1]
            self.query_txt.set(qry_str)
            self.stat_txt.set(data(self.crs, qry, self.trv, self.current_tbls, self.tbls_cols))
        else:
            self.query_txt.set("No tables were chosen")
            self.trv.delete(*self.trv.get_children())
        self.all_related = semQueries.get_all_related(self.current_tbls, self.relations)
        self.add_cmbx['values'] = self.all_related

wind = Window()
