import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
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

    q_data = mycur.execute(query)  # Query's data
    rows = mycur.fetchall()
    c_rows = len(rows)  # Count rows

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
        table_name += f'.{col[0]}'
        tree.heading(idx + 1, text=table_name, anchor="w")
        tree.column(idx + 1, width=88, stretch=NO)

    for row in rows:
        tree.insert('', 'end', values=row)

    semQueries.sort_treeview_by_col(tree, 0, False)
    return f'Columns Count: {len(q_data.description)}\nRows Count: {c_rows}'


def init_window_db(pth):
    """
    Creates all db's vars
    :param pth: DB's path
    :return:    crs (the cursor), all_tbls (list: all tables' names),
                relations (dict: all relations between tables), tbls_cols (dict: Tables with their columns)
    """
    crs = semQueries.db_connector(pth)  # Pointer to DB
    all_tbls = semQueries.tables_names(crs)  # All tables' names
    relations = semQueries.create_tbls_relations(crs, all_tbls)  # Relations between tables (dict)
    tbls_cols = semQueries.tbls_dict(crs, all_tbls)  # Tables with their columns (dict)
    return crs, all_tbls, relations, tbls_cols




def create_txt_lbl(frm, txt, wrpln=450, fnt="Segoe UI", fnt_sz=10, hig=5, anc="w", wid=60, jst='left', lbl_pack=False):
    my_txt = StringVar()
    my_txt.set(txt)
    lbl_txt = Label(frm, textvariable=my_txt, wraplength=wrpln, font=(fnt, fnt_sz),
                    height=hig, anchor=anc, width=wid, justify=jst)
    if lbl_pack:
        lbl_txt.pack()
    return my_txt, lbl_txt


class Window:

    def __init__(self):
        # DB
        self.crs, self.all_tbls, self.relations, self.tbls_cols = init_window_db('CnkDatabase/chinook.db')
        self.current_tbls = []  # Presented tables

        # Window creation
        self.create_root()  # Root

        # Top frame - Will contain combobox, buttons and presents the list of the current tables.
        self.topFrame = Frame(self.root)  # Top frame
        self.topFrame.pack(side="top")

        # Presents the query (lbl will be added)
        self.frm_query = Frame(self.topFrame)
        self.frm_query.grid(row=2, column=0, columnspan=4)
        self.query_txt, self.lbl_query = create_txt_lbl(self.frm_query, "Query will be presented here",
                                                        wid=100, lbl_pack=True)

        # Joined tables text
        self.tbls_join_txt, self.lbl_tbls_join = create_txt_lbl(self.topFrame, 'Joined Tables will be presented here',
                                                                hig=8, wid=35)
        self.lbl_tbls_join.grid(row=1, column=0, sticky="w")

        # Joined columns text
        self.cols_join_txt, self.lbl_cols_join = create_txt_lbl(self.topFrame, 'Joined Columns will be presented here',
                                                                hig=8, wid=35)
        self.lbl_cols_join.grid(row=1, column=1, sticky="w")

        self.create_main_combobox()  # Add Table + Combobox of all tables

        # Bottom frame - Will contain the tree
        self.frm_trv = Frame(self.root)
        self.frm_trv.pack(side='bottom', padx=20, pady=10, fill='both', expand=True)
        self.trv = Treeview(self.frm_trv, columns=(1, 2, 3, 4), height=25, show='headings')
        vsb = ttk.Scrollbar(self.frm_trv, orient="vertical", command=self.trv.yview)
        vsb.pack(side='right', fill='y')  # scrollbar for the tree view vertical
        self.trv.configure(yscrollcommand=vsb.set)
        hsb = ttk.Scrollbar(self.frm_trv, orient="horizontal", command=self.trv.xview)
        hsb.pack(side='bottom', fill='x')  # scrollbar for the tree view horizontal
        self.trv.configure(xscrollcommand=hsb.set)

        self.trv.pack(fill='both', expand=True)  # pack the tree to the frame
        # self.cmbx.bind('<<ComboboxSelect>>', self.cmbx)

        # self.lastClick = '#1'  # representing the last column the user has clicked on (sorting the col in reverse)
        # self.tree.bind("<Button-1>", self.on_click)  # event happening on click on the tree view
        # self.lb1.bind('<<ListboxSelect>>', self.clickListbox1)  # binding click to the 1st listbox
        # self.lb2.bind('<<ListboxSelect>>', self.clickListbox2)  # binding click to the 2nd listbox
        # self.lb3.bind('<<ListboxSelect>>', self.clickListbox3)  # binding click to the 3rd listbox
        # self.value = [None, None, None]  # hold tables marked in the listboxes

        self.root.mainloop()  # Infinite run the program

    def create_root(self, str_title='Seminar Project - Stav Suzan Rabinovich 208661090', size='1000x600'):
        """
        Creates root
        :param str_title: Window's title
        :param size: Window's size
        :return: None
        """
        self.root = Tk()
        self.root.title(str_title)  # Window title
        self.root.geometry(size)  # Window size
        self.root.wm_attributes("-topmost", 1)  # ?

    def create_main_combobox(self):
        self.lbl_add_table = Label(self.topFrame, text="First Table:", height=5, width=10, justify='left')
        self.lbl_add_table.grid(row=0, column=0)
        self.frm_main_cmbx = Frame(self.topFrame)
        self.frm_main_cmbx.grid(row=0, column=1)
        self.main_cmbx = Combobox(self.frm_main_cmbx, values=self.all_tbls, width=30)
        self.main_cmbx.pack()

    def from_cmbx(self, slct_cmbx, event):
        w = event.widget
        val = slct_cmbx.get()
        qry = semQueries.query_creation(self.current_tbls, len(self.current_tbls) + 1,
                                        self.relations, self.tbls_join_txt, self.cols_join_txt)
        qry_str = qry.split("FROM")[0] + '\nFROM' + qry.split("FROM")[1]
        # string_query = query.split("FROM")[0] + '\nFROM' + query.split("FROM")[1]
        # self.var.set(string_query)
        self.var.set(qry_str)
        # self.statistics.set(data(self.my_cursor, query, self.tree, self.value, self.tables_columns))
        self.statistics.set(data(self.crs, qry, self.trv, self.val, self.tbls_cols))
        # self.updateListbox(2, self.relation[self.value[0]])
        # self.updateListbox(3, [])


class App:
    """
    A class used to create an App

    ...

    Methods
    -------
    clickListbox1(event)
        handler for marking value from listbox 1

    clickListbox2(event)
        handler for marking value from listbox 2

    clickListbox3(event)
        handler for marking value from listbox 3

    updateListbox(num, dict_tables)
        updating new items in listbox according to the ones who got clicked

    on_click(event)
        mouse click event handler, sorting the column in treeview whenever clicked
    """

    # def __init__(self):
    # self.var = StringVar()
    # self.label_query = Label(self.frame_query, textvariable=self.var,
    #                          wraplength=450, font=("Arial", 11), height=5, width=50)
    # self.var.set("Query")  # Query label with StringVar
    # self.label_query.pack()
    #
    # self.statistics = StringVar()
    # self.statistics.set('Number of Columns: 0\nNumber of Rows: 0')
    # self.label_statistics = Label(self.topFrame,  # statistics label with StringVar
    #                               textvariable=self.statistics, anchor="nw", wraplength=250, justify='left',
    #                               width=20)
    # self.label_statistics.grid(row=1, column=0, sticky='w', padx=20)

    # self.join_tables = StringVar()
    # self.join_tables.set('Join Columns:\t')  # join tables label with StringVar
    # self.join_tables_label = Label(self.topFrame,
    #                                textvariable=self.join_tables, height=7, anchor="w", width=17, justify='left')
    # self.join_tables_label.grid(row=1, column=1, sticky="w")
    #
    # self.join_columns = StringVar()
    # self.join_columns.set('None')  # join columns label with StringVar
    # self.join_columns_label = Label(self.topFrame,
    #                                 textvariable=self.join_columns, height=7, width=20, anchor="w",
    #                                 justify='left')
    # self.join_columns_label.grid(row=1, column=2, sticky="w")
    #
    # self.lb1_frame = Frame(self.topFrame)
    # self.lb1_frame.grid(row=1, column=3, padx=5)  # frame and Listbox for the 1st table pick
    # self.lb1 = Listbox(self.lb1_frame, exportselection=0, width=20)
    # for i in range(0, len(tables)):  # inserting to the first listbox all the table names in the DB
    #     self.lb1.insert(i, tables[i])
    # self.lb1.pack(side='left')

    # self.lb2_frame = Frame(self.topFrame)
    # self.lb2_frame.grid(row=1, column=4, padx=5)  # frame and Listbox for the 2nd table pick
    # self.lb2 = Listbox(self.lb2_frame, exportselection=0, width=20)
    # self.lb2.pack(side='left')
    #
    # self.lb3_frame = Frame(self.topFrame)
    # self.lb3_frame.grid(row=1, column=5, padx=5)  # frame and Listbox for the 3rd table pick
    # self.lb3 = Listbox(self.lb3_frame, exportselection=0, width=20)
    # self.lb3.pack(side='left')

    # vsb_lb1 = ttk.Scrollbar(self.lb1_frame, orient="vertical", command=self.lb1.yview)
    # vsb_lb1.pack(side='right', fill='y')  # scrollbar to move around the 1st listbox
    # self.lb1.config(yscrollcommand=vsb_lb1.set)
    #
    # vsb_lb2 = ttk.Scrollbar(self.lb2_frame, orient="vertical", command=self.lb2.yview)
    # vsb_lb2.pack(side='right', fill='y')  # scrollbar to move around the 2nd listbox
    # self.lb2.config(yscrollcommand=vsb_lb2.set)
    #
    # vsb_lb3 = ttk.Scrollbar(self.lb3_frame, orient="vertical", command=self.lb3.yview)
    # vsb_lb3.pack(side='right', fill='y')  # scrollbar to move around the 3rd listbox
    # self.lb3.config(yscrollcommand=vsb_lb3.set)

    # self.label_table1 = Label(self.topFrame, text="Table 1", font=("Arial", 11))
    # self.label_table1.grid(row=0, column=3)  # label for the 1st Table
    #
    # self.label_table2 = Label(self.topFrame, text="Table 2", font=("Arial", 11))
    # self.label_table2.grid(row=0, column=4)  # label for the 2nd Table
    #
    # self.label_table3 = Label(self.topFrame, text="Table 3", font=("Arial", 11))
    # self.label_table3.grid(row=0, column=5)  # label for the 3rd Table
    #
    # self.tree_frame = Frame(self.root)
    # # pack the frame where the tree will be held(under top frame)
    # self.tree_frame.pack(side="bottom", padx=30, pady=15, fill='both', expand=True)
    # # creating a new tree
    # self.tree = ttk.Treeview(self.tree_frame, columns=(1, 2, 3), height=20, show="headings")
    #
    # vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
    # vsb.pack(side='right', fill='y')  # scrollbar for the tree view vertical
    # self.tree.configure(yscrollcommand=vsb.set)
    #
    # hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
    # hsb.pack(side='bottom', fill='x')  # scrollbar for the tree view horizontal
    # self.tree.configure(xscrollcommand=hsb.set)
    #
    # self.tree.pack(fill='both', expand=True)  # pack the tree to the frame
    #
    # self.lastClick = '#1'  # representing the last column the user has clicked on (sorting the col in reverse)
    # self.tree.bind("<Button-1>", self.on_click)  # event happening on click on the tree view
    #
    # self.lb1.bind('<<ListboxSelect>>', self.clickListbox1)  # binding click to the 1st listbox
    # self.lb2.bind('<<ListboxSelect>>', self.clickListbox2)  # binding click to the 2nd listbox
    # self.lb3.bind('<<ListboxSelect>>', self.clickListbox3)  # binding click to the 3rd listbox
    #
    # self.value = [None, None, None]  # hold tables marked in the listboxes
    #
    # self.root.mainloop()  # Infinite run the program

    def clickListbox1(self, event):
        """Gets event
        listbox mark table event handler, showing query result from database to the treeview
        and updating the 2nd listbox to show new tables"""
        w = event.widget
        index = int(w.curselection()[0])
        self.value[0] = w.get(index)
        self.value[1] = None
        self.value[2] = None
        query = semQueries.query_creation(self.value, 1, self.relation, self.join_columns, self.join_tables)
        string_query = query.split("FROM")[0] + '\nFROM' + query.split("FROM")[1]
        self.var.set(string_query)
        self.statistics.set(data(self.my_cursor, query, self.tree, self.value, self.tables_columns))
        self.updateListbox(2, self.relation[self.value[0]])
        self.updateListbox(3, [])

    def clickListbox2(self, event):
        """Gets event
                listbox mark table event handler, showing query result from database to the treeview
                and updating the 3rd listbox to show new tables"""
        w = event.widget
        index = int(w.curselection()[0])
        self.value[1] = w.get(index)
        self.value[2] = None
        query = semQueries.query_creation(self.value, 2, self.relation, self.join_columns, self.join_tables)
        from_split = query.split("FROM")
        string_query = from_split[0] + '\nFROM' + from_split[1].split("WHERE")[0] + '\nWHERE' + \
                       from_split[1].split("WHERE")[1]
        self.var.set(string_query)
        self.statistics.set(data(self.my_cursor, query, self.tree, self.value, self.tables_columns))
        self.updateListbox(3, self.relation[self.value[1]])

    def clickListbox3(self, event):
        """Gets event
            listbox mark table event handler, showing query result from database to the treeview
            """
        w = event.widget
        index = int(w.curselection()[0])
        self.value[2] = w.get(index)
        query = semQueries.query_creation(self.value, 3, self.relation, self.join_columns, self.join_tables)
        from_split = query.split("FROM")
        string_query = from_split[0] + '\nFROM' + from_split[1].split("WHERE")[0] + '\nWHERE' + \
                       from_split[1].split("WHERE")[1]
        self.var.set(string_query)
        self.statistics.set(data(self.my_cursor, query, self.tree, self.value, self.tables_columns))

    def updateListbox(self, num, dict_tables):
        """Updating new items in listbox according to the ones who got clicked

                        Parameters
                        ----------
                        num : int
                            integer showing what listbox needed to be updated
                        dict_tables: dictionary(string:string)
                            dictionary representing the tables that can join to the current table
                    """
        lb = [self.lb1, self.lb2, self.lb3]
        if num < 1:
            return
        lb[num - 1].delete(0, END)
        for index, key in enumerate(dict_tables):
            if key not in self.value:
                lb[num - 1].insert(index, key)

    def on_click(self, event):
        """Mouse click event handler, sorting the column in treeview whenever clicked

                Parameters
                ----------
                event : event
                    event showing info about the mouse click
            """
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            col = self.tree.identify_column(event.x)
            if self.lastClick is None or self.lastClick != col:
                self.tree.heading(col, command=lambda: semQueries.sort_treeview_by_col(self.tree, col, False))
                self.lastClick = col


# app = App()
wind = Window()
