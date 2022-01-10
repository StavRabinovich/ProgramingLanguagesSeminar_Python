import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview, Scrollbar
import seminarFunctions


def data(mycur, query, tree, current_tbls, table_columns):
    """
    Import data using query, and adding to the tree (sorted)
    :param mycur:           my cursor
    :param query:           (String) the query
    :param tree:            (treeview) UI of the query results
    :param current_tbls:    list of tables in current query
    :param table_columns:   (dict) tables and their cols' names
    :return:                (String) num of cols AND num of imported rows
    """
    for x in tree.get_children():
        tree.delete(x)

    query = query.replace('main.', '')
    q_data = mycur.execute(query)  # Query's data
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

    print(f'Number of Columns: {len(q_data.description)}\t\t\tNumber of Rows: {len(rows)}')
    return f'Number of Columns: {len(q_data.description)}\t\t\tNumber of Rows: {len(rows)}'



class Window:
    def __init__(self):
        self.init_window('CnkDatabase/chinook.db')
        self.init_combos()
        self.init_info()
        self.init_treeview()  # Bottom frame - Contains the treeview
        self.root.mainloop()  # Infinite run the program

    def init_window(self, pth):
        """
                Creates all db's vars
                :param pth: DB's path
                :return:    None
                """
        # DB Init
        self.crs = seminarFunctions.db_connector(pth)  # Pointer to DB
        self.all_tbls = seminarFunctions.tables_names(self.crs)  # All tables' names
        self.relations = seminarFunctions.create_tbls_relations(self.crs, self.all_tbls)  # Relations between tables (dict)
        self.tbls_cols = seminarFunctions.tbls_dict(self.crs, self.all_tbls)  # Tables with their columns (dict)
        self.current_tbls = []  # Holds all current queries' tables
        self.all_related = []  # Holds all related tables to current tables

        # Root Init
        self.root = Tk()
        self.root.title('ChinookDB JOIN Queries')  # Window title
        self.root.geometry('1100x700')  # Window size
        self.root.wm_minsize(width=1000, height=700)  # Window MIN size
        self.root.wm_attributes("-topmost", 1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Frames Init
        self.frm_user_choice = Frame(self.root, width=270, height=160, pady=1, padx=1)
        self.frm_stats = Frame(self.root, width=720, height=20, pady=1, padx=1,
                               highlightbackground="midnightblue", highlightthickness=1)
        self.frm_tbls_join = Frame(self.root, width=270, height=140, pady=1, padx=1)
        self.frm_query = Frame(self.root, width=720, height=310, padx=1, pady=1)
        self.frm_trv = Frame(self.root, width=1000, height=360, padx=1, pady=1)
        self.frm_user_choice.grid(row=0, sticky='new', rowspan=2, padx=20, pady=20)
        self.frm_stats.grid(row=0, column=1, sticky='ew', padx=20, pady=20)
        self.frm_tbls_join.grid(row=1, column=0, sticky='sew', padx=20)
        self.frm_query.grid(row=1, column=1, columnspan=3, sticky='sew', padx=20)
        self.frm_trv.grid(row=2, column=0, rowspan=4, columnspan=5, sticky='new', padx=20, pady=20)

    def init_combos(self):
        """
        Init comboboxes, buttons and labels that are related to user's choices
        :return:
        """
        self.frm_combos = Frame(self.frm_user_choice)
        self.frm_combos.pack()

        # 1st Combobox
        self.lbl_main_table = Label(self.frm_combos, text="First Table:", height=2, width=10, fg='midnightblue')
        self.frm_main_cmbx = Frame(self.frm_combos)
        self.main_cmbx = Combobox(self.frm_main_cmbx, values=self.all_tbls, width=25)
        self.lbl_main_table.grid(row=0, column=0)   # Label Location
        self.frm_main_cmbx.grid(row=0, column=1)    # Combobox Location
        self.main_cmbx.pack()

        # 2nd Combobox
        self.lbl_add_tbls = Label(self.frm_combos, text="Add Table:", height=2, width=10, fg='midnightblue')
        self.frm_add_cmbx = Frame(self.frm_combos)
        self.add_cmbx = Combobox(self.frm_add_cmbx, values=self.all_related, width=25)
        self.lbl_add_tbls.grid(row=1, column=0)  # Label Location
        self.frm_add_cmbx.grid(row=1, column=1)  # Combobox Location
        self.add_cmbx.pack()

        # Buttons
        self.frm_btns = Frame(self.frm_combos)
        self.frm_btns.grid(row=2, column=0, columnspan=2)
        self.undo_btn = Button(self.frm_btns, text='Undo', width=10, command=self.cmnd_undo)
        self.reset_btn = Button(self.frm_btns, text='Reset', width=10, command=self.cmnd_reset)
        self.undo_btn.pack(side='left', padx=10, pady=15)
        self.reset_btn.pack(side='right', padx=10, pady=15)
        self.main_cmbx.bind("<<ComboboxSelected>>", self.first_choice)  # Command
        self.add_cmbx.bind("<<ComboboxSelected>>", self.add_from_cmbx)  # Command

    def init_info(self):
        """
        Initiates Text Widgets and statistics' label on window
        :return: None
        """
        self.txt_query, self.scb_query = seminarFunctions.create_text_wid(
            self.frm_query, 'Query will be presented here', 11, 95)     # Init Query's text widget
        self.txt_info, self.scb_info = seminarFunctions.create_text_wid(
            self.frm_tbls_join, 'No Tables!', 8, 43)                    # Init Tables' text widget
        # Init statistics line
        self.stat_txt, self.stat_lbl = seminarFunctions.create_txt_lbl(
            self.frm_stats, 'Number of Columns: 0 \t\t\tNumber of Rows: 0', wrpln=1000, wid=95, hig=1, anc="nw")
        self.stat_lbl.grid(row=0, column=1, sticky='ew', padx=10, pady=10)

    def init_treeview(self):
        """
        Initiates Treeview
        :return: None
        """
        self.trv = Treeview(self.frm_trv, height=16, show='headings')                   # Treeview
        vsb = ttk.Scrollbar(self.frm_trv, orient="vertical", command=self.trv.yview)    # Treeview vertical scrollbar
        hsb = ttk.Scrollbar(self.frm_trv, orient="horizontal", command=self.trv.xview)  # Treeview horizontal scrollbar
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.trv.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)              # Scrollbars
        self.trv.pack(fill='both', expand=True)

        self.lastClick = '#1'                       # Last clicked column (sorting the col in reverse)
        self.trv.bind("<Button-1>", self.trv_click)  # event happening on click on the tree view

    def first_choice(self, event):
        """
        Inserts the first table to query
        :param event:
        :return:
        """
        self.current_tbls = []
        self.add_from_cmbx(event)

    def add_from_cmbx(self, event):
        """
        Adding table to query by user's choice
        :param event: (event) Presents the name of the chosen table
        :return: None
        """
        self.current_tbls.append(event.widget.get())
        self.add_cmbx.set('')
        self.update_query()

    def trv_click(self, event):
        """
        Sorting by clicked column in TreeView
        :param event:   (event) Presenting info about mouse's click
        :return:
        """
        rgn = self.trv.identify("region", event.x, event.y)
        if rgn == "heading":
            col = self.trv.identify_column(event.x)
            if self.lastClick is None or self.lastClick != col:
                self.trv.heading(col, command=lambda: self.sort_treeview_by_col(col, False))
                self.lastClick = col

    def cmnd_undo(self):
        """
        Remove last added table
        :return: None
        """
        if self.current_tbls:
            self.current_tbls.pop()
        if not self.current_tbls:
            self.cmnd_reset()
        else:
            self.add_cmbx.set('')
            self.update_query()

    def cmnd_reset(self):
        """
        Resets Window
        :return: None
        """
        self.current_tbls = []
        self.stat_txt.set('Number of Columns: 0 \t\t\tNumber of Rows: 0')
        self.main_cmbx.set('')
        self.txt_info.config(state=NORMAL)
        self.txt_info.delete('1.0', 'end')
        self.txt_info.insert(tkinter.END, 'No tables were chosen!')
        self.txt_info.config(state=DISABLED)
        self.update_query()

    def remove_last_table(self):
        """
        Removes the last table from tables' list
        :return: None
        """
        if self.current_tbls:
            self.current_tbls.pop()
        self.update_query()

    def update_query(self):
        """
        Updated the query by new changes
        :return: None
        """
        self.txt_query.config(state=NORMAL)
        self.txt_query.delete('1.0', 'end')
        if self.current_tbls:
            qry = seminarFunctions.query_creation(
                self.current_tbls, len(self.current_tbls), self.relations, self.txt_info)   # Creates query
            qry_str = seminarFunctions.query_format(qry)                                    # Creates query in format
            self.txt_query.insert('0.0', qry_str)                            # Insert formatted query to app's window
            self.stat_txt.set(data(self.crs, qry_str, self.trv, self.current_tbls, self.tbls_cols))
        else:
            self.txt_query.insert('1.0', "No tables were chosen!")
            self.trv.delete(*self.trv.get_children())                               # Remove unrelated from treeview
        self.txt_query.config(state=DISABLED)
        # Updates tables that Related to the chosen tables
        self.all_related = seminarFunctions.get_all_related(self.current_tbls, self.relations)
        self.add_cmbx['values'] = self.all_related

    def sort_treeview_by_col(self, col, rvs):
        """
        Sorting treeview by cols & reverse
        :param col: (int) Index of col in trv
        :param rvs: (boolean) Reverse
        :return:    None
        """
        lst = [(self.trv.set(k, col), k) for k in self.trv.get_children('')]
        try:
            lst.sort(key=lambda x: int(x[0]), reverse=rvs)
        except ValueError:
            lst.sort(reverse=rvs)
        for index, (val, k) in enumerate(lst):
            self.trv.move(k, '', index)  # Put in sorted placement
        self.trv.heading(col, command=lambda: self.sort_treeview_by_col(col, not rvs))  # Reverse next time


wind = Window()
