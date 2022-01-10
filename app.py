import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview, Scrollbar
import semQueries


def create_button(frm, txt, cmnd, width=10, bg='lavender'):
    return Button(frm, text=txt, width=width, command=cmnd, bg=bg)


def query_format(str):
    dct = {'FROM': '\nFROM', ' WHERE': '\nWHERE', ' AND ': '\nAND '}
    for r in (('FROM', '\nFROM'), (' WHERE', '\nWHERE'), (' AND ', '\nAND ')):
        str = str.replace(*r)
    return str


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

    semQueries.sort_treeview_by_col(tree, 0, False)
    print(f'Columns Count: {len(q_data.description)}\tRows Count: {len(rows)}')
    return f'Columns Count: {len(q_data.description)}\tRows Count: {len(rows)}'


def create_txt_lbl(frm, txt, wrpln=250, fnt="Segoe UI", fnt_sz=10, hig=5, anc="w", wid=20, jst='left', lbl_pack=False):
    """
    Create labels with text inside
    :param frm:         Father frame
    :param txt:         Label's value
    :param wrpln:       wraplength
    :param fnt:         Font
    :param fnt_sz:      Font size
    :param hig:         height
    :param anc:         anchor
    :param wid:         width
    :param jst:         justify
    :param lbl_pack:    if needed to be packed
    :return: my_text (StringVar), lbl_text (Label)
    """
    my_txt = StringVar()
    my_txt.set(txt)
    lbl_txt = Label(frm, textvariable=my_txt, wraplength=wrpln, font=(fnt, fnt_sz),
                    height=hig, anchor=anc, width=wid, justify=jst)
    if lbl_pack:
        lbl_txt.pack()
    return my_txt, lbl_txt


def create_text(master, str, height=10, width=110, font=("Segoe UI", 10), bgcolor='whitesmoke'):
    frm = Frame(master)
    txt = Text(frm, height=height, width=width)
    txt.pack(side=LEFT)
    txt.configure(font=font, background=bgcolor)
    txt.insert(tkinter.END, str)
    scb = None
    # scb = Scrollbar(frm, command=txt.yview)
    # scb.pack(side=RIGHT)
    return frm, txt, scb


class Window:
    def __init__(self):
        self.init_window_db('CnkDatabase/chinook.db')  # DB connection
        self.all_tbls = []
        self.init_root()  # Root / Window creation
        self.init_combos()
        self.init_topframe()  # Top frame - Contains comboboxes, buttons and visual text
        self.init_treeview()  # Bottom frame - Contains the treeview
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
        self.all_related = []  # Holds all related tables to current tables

    def init_root(self):
        """
        Creates root
        :return: None
        """
        self.root = Tk()
        self.root.title('ChinookDB JOIN Queries')  # Window title
        self.root.geometry('850x600')  # Window size
        self.root.wm_minsize(width=850, height=550)  # Window MIN size
        self.root.wm_attributes("-topmost", 1)

    def init_combos(self):
        self.topFrame = Frame(self.root, background="lightsteelblue")
        self.topFrame.pack(pady=20)
        self.topFrame.grid(sticky=NW, ipadx=20)
        self.frm_combos = Frame(self.topFrame, background="lightsteelblue")
        self.frm_combos.pack(pady=20)

        # 1st Combobox
        self.lbl_main_table = Label(self.frm_combos, text="First Table:", height=2, width=10,
                                    justify='left', bg="lightsteelblue", fg='midnightblue')
        self.frm_main_cmbx = Frame(self.frm_combos)
        self.main_cmbx = Combobox(self.frm_main_cmbx, values=self.all_tbls, width=25)
        self.lbl_main_table.grid(row=0, column=0)  # Location
        self.frm_main_cmbx.grid(row=0, column=1)  # Location
        self.main_cmbx.pack()

        # 2nd Combobox
        self.lbl_add_tbls = Label(self.frm_combos, text="Add Table:", height=2, width=10,
                                  justify='left', bg='lightsteelblue', fg='midnightblue')
        self.frm_add_cmbx = Frame(self.frm_combos)
        self.add_cmbx = Combobox(self.frm_add_cmbx, values=self.all_related, width=25)
        self.lbl_add_tbls.grid(row=1, column=0)  # Location
        self.frm_add_cmbx.grid(row=1, column=1)  # Location
        self.add_cmbx.pack()

        # Buttons
        self.frm_btns = Frame(self.frm_combos, background="lightsteelblue")
        self.frm_btns.grid(row=2, column=0, columnspan=2)
        self.undo_btn = create_button(self.frm_btns, 'Undo', self.cmnd_undo)
        self.reset_btn = create_button(self.frm_btns, 'Reset', self.cmnd_reset)
        self.undo_btn.pack(side='left', padx=10, pady=25)
        self.reset_btn.pack(side='right', padx=10, pady=25)
        self.main_cmbx.bind("<<ComboboxSelected>>", self.first_choice)
        self.add_cmbx.bind("<<ComboboxSelected>>", self.add_from_cmbx)

    def init_topframe(self):
        # Top frame - Will contain combobox, buttons and presents the list of the current tables.

        # Presents the query (lbl will be added)
        self.frm_query, self.txt_query, self.scb_query = create_text(self.root, "Query will be presented here")
        self.frm_query.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.frm_info = Frame(self.root, background='yellow')
        self.frm_info.grid(row=0, column=1, sticky=NE)
        # self.scb_info = Scrollbar(self.frm_info)
        # self.scb_info.pack(side=RIGHT, fill=Y)

        self.cnvs_info = Canvas(self.frm_info, bg='red', height=170)
        self.vsb_info = Scrollbar(self.frm_info, orient='vertical', command=self.cnvs_info.yview)
        # Joined tables text
        # self.tbls_join_txt, self.lbl_tbls_join = create_txt_lbl(
        #     self.frm_info, 'Joined Tables will be here', hig=7, wid=75)

        self.tbls_join_txt = StringVar()
        self.tbls_join_txt.set('Joined Tables will be presented here')
        self.lbl_tbls_join = Label(self.cnvs_info, textvariable=self.tbls_join_txt, width=80, height=30, anchor='w')
        self.lbl_tbls_join.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.cnvs_info.create_window(1, 50, anchor='nw', window=self.lbl_tbls_join, height=10)

        self.cnvs_info.configure(scrollregion=self.cnvs_info.bbox('all'), yscrollcommand=self.vsb_info.set)

        self.cnvs_info.pack(fill='both', expand=True, side='left', pady=10)
        self.vsb_info.pack(fill='y', side='right')

        # Statistics
        self.stat_txt = StringVar()
        self.stat_txt.set('Number of Columns: 0 Number of Rows: 0')
        self.stat_lbl = Label(self.cnvs_info, textvariable=self.tbls_join_txt, width=80, height=1, anchor='nw')
        # self.stat_lbl.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.cnvs_info.create_window(2, 100, anchor='nw', window=self.lbl_tbls_join, height=10)
        # self.stat_txt, self.stat_lbl = create_txt_lbl(
        # self.frm_info, 'Number of Columns: 0 Number of Rows: 0', wrpln=1000, wid=75, hig=1, anc="nw")
        # self.stat_lbl.grid(row=0, column=1, sticky='w', padx=10, pady=10)

    def init_treeview(self):
        self.frm_trv = Frame(self.root)
        self.frm_trv.grid(row=2, column=0, columnspan=4, padx=20, pady=10)
        # self.frm_trv.pack(expand=True)
        # self.frm_trv.pack(side='bottom', padx=20, pady=10, fill='both', expand=True)
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
