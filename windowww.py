import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview, Scrollbar
import semQueries


myfont = ('Segoe UI', 10)


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


def create_text(master, str, height=10, width=70, font=("Segoe UI", 10), bgcolor='whitesmoke'):
    frm = Frame(master)
    txt = Text(frm, height=height, width=width)
    txt.pack(side=LEFT)
    txt.configure(font=font, background=bgcolor)
    txt.insert(tkinter.END, str)
    scb = Scrollbar(frm)
    scb.pack(side=RIGHT)
    return frm, txt, scb


class Visual:
    def __init__(self):
        self.init_window_db('CnkDatabase/chinook.db')  # DB connection
        self.init_root()  # Root / Window creation
        self.init_combos()
        # self.init_topframe()  # Top frame - Contains comboboxes, buttons and visual text
        # self.init_treeview()  # Bottom frame - Contains the treeview
        # self.main_cmbx.bind("<<ComboboxSelected>>", self.first_choice)
        # self.add_cmbx.bind("<<ComboboxSelected>>", self.add_from_cmbx)

        self.root.mainloop()  # Infinite run the program

    def init_combos(self):
        self.topFrame = Frame(self.root, background="lightsteelblue")
        self.topFrame.pack(pady=20)
        self.topFrame.grid(sticky=NW, ipadx=20)
        self.frm_combos = Frame(self.topFrame, background="lightsteelblue")
        self.frm_combos.pack(pady=20)

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
        self.root.geometry('1000x600')  # Window size
        self.root.wm_minsize(width=900, height=550)  # Window MIN size
        self.root.wm_attributes("-topmost", 1)

    def init_topframe(self):
        # Top frame:
        self.topFrame = Frame(self.root)  # Top frame
        self.topFrame.pack()

        self.frm_requests = Frame(self.topFrame, bd=1, relief=SOLID, padx=10, pady=10)
        self.frm_requests.place(x=30, y=30)
        self.init_main_combobox() # Add Combobox of all tables

        # self.frm_requests = Frame(self.topFrame, bd=1, relief=SOLID, padx=10, pady=10)
        # self.frm_requests.place(x=30, y=30)
        # self.init_main_combobox()  # Add Combobox of all tables
        # self.init_extra_tables()  # Add Combobox and buttons
        #
        # Presents the query (lbl will be added)
        # self.frm_query, self.txt_query, self.scb_query = create_text(self.topFrame, "Query will be presented here")
        # self.frm_query.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Joined tables text
        # self.tbls_join_txt, self.lbl_tbls_join = create_txt_lbl(
        #     self.topFrame, 'Joined Tables will be here', hig=8, wid=50)
        # self.lbl_tbls_join.grid(row=2, column=3, columnspan=2, sticky="w", padx=10, pady=10)
        #
        # Statistics
        # self.stat_txt, self.stat_lbl = create_txt_lbl(
        #     self.topFrame, 'Number of Columns: 0 Number of Rows: 0', wrpln=100, wid=60, hig=2, anc="nw")
        # self.stat_lbl.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=10)

    def init_main_combobox(self):
        self.lbl_main_table = Label(self.frm_requests, text="First Table:", height=2, width=10, justify='left')
        self.frm_main_cmbx = Frame(self.frm_requests)
        self.main_cmbx = Combobox(self.frm_main_cmbx, values=self.all_tbls, width=20)
        self.lbl_main_table.grid(row=0, column=0, pady=20)  # Location
        self.frm_main_cmbx.grid(row=0, column=1, pady=10)  # Location
        self.main_cmbx.pack()
        # Combobox
        self.lbl_add_tbls = Label(self.frm_requests, text="Add Table:", height=2, width=10, justify='left')\
            .grid(row=0, column=2)  # Location
        self.frm_add_cmbx = Frame(self.frm_requests)
        self.add_cmbx = Combobox(self.frm_add_cmbx, values=self.all_related, width=20)
        self.frm_add_cmbx.grid(row=0, column=3)  # Location
        self.add_cmbx.pack()


vsl = Visual()


class Window:

    def __init__(self):
        self.init_window_db('CnkDatabase/chinook.db')  # DB connection
        self.init_root()  # Root / Window creation
        self.init_topframe()  # Top frame - Contains comboboxes, buttons and visual text
        self.init_treeview()  # Bottom frame - Contains the treeview

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
        self.all_related = []  # Holds all related tables to current tables

    def init_root(self):
        """
        Creates root
        :return: None
        """
        self.root = Tk()
        self.root.title('ChinookDB JOIN Queries')  # Window title
        self.root.geometry('1000x600')  # Window size
        self.root.wm_minsize(width=900, height=550)  # Window MIN size
        self.root.wm_attributes("-topmost", 1)

    def init_topframe(self):
        # Top frame - Will contain combobox, buttons and presents the list of the current tables.
        self.topFrame = Frame(self.root)  # Top frame
        self.topFrame.pack()
        self.frm_requests = Frame(self.topFrame, bd=1, relief=SOLID, padx=10, pady=10)
        self.frm_requests.place(x=30, y=30)
        self.init_main_combobox()  # Add Combobox of all tables
        self.init_extra_tables()  # Add Combobox and buttons

        # Presents the query (lbl will be added)
        # self.frm_query, self.txt_query, self.scb_query = create_text(self.topFrame, "Query will be presented here")
        # self.frm_query.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Joined tables text
        self.tbls_join_txt, self.lbl_tbls_join = create_txt_lbl(
            self.topFrame, 'Joined Tables will be here', hig=8, wid=50)
        self.lbl_tbls_join.grid(row=2, column=3, columnspan=2, sticky="w", padx=10, pady=10)

        # Statistics
        self.stat_txt, self.stat_lbl = create_txt_lbl(
            self.topFrame, 'Number of Columns: 0 Number of Rows: 0', wrpln=100, wid=60, hig=2, anc="nw")
        self.stat_lbl.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=10)

    def init_main_combobox(self):
        self.lbl_main_table = Label(self.frm_requests, text="First Table:", height=2, width=10, justify='left')
        self.frm_main_cmbx = Frame(self.frm_requests)
        self.main_cmbx = Combobox(self.frm_main_cmbx, values=self.all_tbls, width=20)
        self.lbl_main_table.grid(row=0, column=0, pady=20)  # Location
        self.frm_main_cmbx.grid(row=0, column=1, pady=10)  # Location
        self.main_cmbx.pack()

    def init_extra_tables(self):
        """
        Init window features for adding another table(s) / removing table(s)
        :return: None
        """
        # Combobox
        self.lbl_add_tbls = Label(self.frm_requests, text="Add Table:", height=2, width=10, justify='left')\
            .grid(row=0, column=2)  # Location
        self.frm_add_cmbx = Frame(self.frm_requests)
        self.add_cmbx = Combobox(self.frm_add_cmbx, values=self.all_related, width=20)
        self.frm_add_cmbx.grid(row=0, column=3)  # Location
        self.add_cmbx.pack()

        # Buttons
        self.frm_btns = Frame(self.frm_requests)
        self.frm_btns.grid(row=0, column=4)
        self.undo_btn = Button(self.frm_btns, text="Undo", width=10, command=self.cmnd_undo)  # Undo button
        self.reset_btn = Button(self.frm_btns, text="Reset", width=10, command=self.cmnd_reset)  # Reset button
        self.undo_btn.pack(side='left')
        self.reset_btn.pack(side='right')

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


# wind = Window()

ws = Tk()
ws.title('Email System')
ws.geometry('940x500')
ws.config(bg='#f7ef38')

variable = StringVar()
gender = ('Male', 'Female', 'Other')
variable.set(gender[0])

# widgets
left_frame = Frame(ws, bd=1, relief=SOLID, padx=10, pady=10)

Label(left_frame, text="Enter Email", font=('Times', 14)).grid(row=0, column=0, sticky=W, pady=10)
Label(left_frame, text="Enter Password", font=('Times', 14)).grid(row=1, column=0, pady=10)
log_em = Entry(left_frame, font=('Times', 14))
log_pw = Entry(left_frame, font=('Times', 14))
login_btn = Button(left_frame, width=15, text='Login', font=('Times', 14), command=None)
#
right_frame = Frame(ws, bd=2, relief=SOLID, padx=10, pady=10)

Label(right_frame, text="Enter Name", font=('Times', 14)).grid(row=0, column=0, sticky=W, pady=10)
Label(right_frame, text="Enter Email", font=('Times', 14)).grid(row=1, column=0, sticky=W, pady=10)
Label(right_frame, text="Enter Mobile", font=('Times', 14)).grid(row=2, column=0, sticky=W, pady=10)
Label(right_frame, text="Enter Age", font=('Times', 14)).grid(row=3, column=0, sticky=W, pady=10)
Label(right_frame, text="Select Gender", font=('Times', 14)).grid(row=4, column=0, sticky=W, pady=10)
Label(right_frame, text="Enter Password", font=('Times', 14)).grid(row=5, column=0, sticky=W, pady=10)
Label(right_frame, text="Re-Enter Password", font=('Times', 14)).grid(row=6, column=0, sticky=W, pady=10)

reg_na = Entry(right_frame, font=('Times', 14))
reg_em = Entry(right_frame, font=('Times', 14))
reg_mo = Entry(right_frame, font=('Times', 14))
reg_ag = Entry(right_frame, font=('Times', 14))
reg_ge = OptionMenu(right_frame, variable, *gender)
reg_ge.config(width=10, font=('Times', 14))
reg_pw = Entry(right_frame, font=('Times', 14))
re_pw = Entry(right_frame, font=('Times', 14))

reg_btn = Button(right_frame, width=15, text='Register', font=('Times', 14), command=None)

# widgets placement
log_em.grid(row=0, column=1, pady=10, padx=20)
log_pw.grid(row=1, column=1, pady=10, padx=20)
login_btn.grid(row=2, column=1, pady=10, padx=20)
left_frame.place(x=30, y=30)

#
reg_na.grid(row=0, column=1, pady=10, padx=20)
reg_em.grid(row=1, column=1, pady=10, padx=20)
reg_mo.grid(row=2, column=1, pady=10, padx=20)
reg_ag.grid(row=3, column=1, pady=10, padx=20)
reg_ge.grid(row=4, column=1, pady=10, padx=20)
reg_pw.grid(row=5, column=1, pady=10, padx=20)
re_pw.grid(row=6, column=1, pady=10, padx=20)
reg_btn.grid(row=7, column=1, pady=10, padx=20)
right_frame.place(x=500, y=50)

# infinite loop
ws.mainloop()