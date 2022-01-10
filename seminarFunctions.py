import sqlite3
import tkinter
from tkinter import *

myfont = ("Segoe UI", 10)   # Font


def db_connector(db):
    """
    Pointing to DB
    :param db:      (string) path to DB location
    :return:        cursor pointing to DB
    """
    conn = sqlite3.connect(db)
    return conn.cursor()


def tables_names(cur):
    """
    Creates list of all tables names
    :param cur:     cursor
    :return:        tbls - list of tables names
    """
    tbls = []
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for row in res.fetchall():
        if row[0] != 'sqlite_sequence' and row[0] != 'sqlite_stat1':
            tbls.append(row[0])
    return tbls


def str_to_sql(s):   # From string to sql
    return '"' + s.replace('"', '""') + '"'


def create_tbls_relations(cur, tbls):
    """
    Creating dict with table and their FKs
    :param cur:     Mouse cursor handler
    :param tbls:    list of tables' names in DB
    :return:        (dict) rlts { TableName : (list) FKs }
    """
    rlts = dict()
    for tbl in tbls:
        rlts[tbl] = dict()  # Creates dict() for table in dictionary
    for tbl in tbls:
        rows = cur.execute("PRAGMA foreign_key_list({})".format(str_to_sql(tbl)))
        for r in rows.fetchall():
            rlts[r[2]][tbl] = r[4]  # table2Name : (table1Name : FK)
            rlts[tbl][r[2]] = r[3]  # table1Name : (table2Name : FK)
    return rlts


def find_related_tbl(tbl, tbls, relations):
    """
    finds the related table
    :param tbl:         Table's name that need to be connected
    :param tbls:        List of all optional tables
    :param relations:   Relations dictionary
    :return:            (String) FK
    """
    for rlt_tbl in tbls:
        if tbl in relations[rlt_tbl] and rlt_tbl is not tbl:
            return rlt_tbl
    return None


def query_creation(tbls, tbls_num, relations, txt_wdg):
    """
    Creates query from tables and relation
    :param tbls:        list of tables' names in DB
    :param tbls_num:    (int) number of current tables.
    :param relations:   (dict) dictionary of dictionaries of table, it fk and connected tables.
    :param txt_wdg:     (Text Widget) Text widget that presents the tables to the use
    :return:            (String) The query
    """
    # Query's base
    tbls_set = set()        # Set of all related tables (without duplicates)
    tbls_set.add(tbls[0])
    q_where = f' WHERE '
    str_relation = ''
    for i in range(tbls_num - 1):
        if 0 < i:           # Add one more table
            q_where += ' AND '
            str_relation += '\n\n'
        rlt_tbl = find_related_tbl(tbls[i], tbls, relations)
        tbls_set.add(tbls[i])   # Add to set
        tbls_set.add(rlt_tbl)   # Add to set
        str_relation += f'Tables: {tbls[i]}, {rlt_tbl} \tFK: {relations[tbls[i]][rlt_tbl]}'
        q_where += f'{tbls[i]}.{relations[tbls[i]][rlt_tbl]} = {rlt_tbl}.{relations[rlt_tbl][tbls[i]]}'

    if tbls_num == 1:
        q_where = ''
        str_relation = 'No Joined tables'
    txt_wdg.config(state=NORMAL)                # Writes to text widget
    txt_wdg.delete('1.0', 'end')
    txt_wdg.insert(tkinter.END, str_relation)
    txt_wdg.config(state=DISABLED)

    q_select = f'SELECT * FROM {tbls[0]}'
    for tbl in tbls_set:
        if tbl is not tbls[0]:
            q_select += f', {tbl}'

    return q_select + q_where


def tbls_dict(cur, tbls):
    """
    Dict of tables with their cols
    :param cur:     Cursor
    :param tbls:    List of all tables' names
    :return:    (dict)  d_tables (table : columns)
    """
    d_tables = dict()
    for t in tbls:
        d_tables[t] = []
        cols = cur.execute(f"pragma table_info({t})")
        for col in cols.fetchall():
            d_tables[t].append(col[1])
    return d_tables


def get_all_related(current_tbls, d_rlts):
    """
    Add all related tables to a list
    :param current_tbls:
    :param d_rlts:
    :return:list of all related tables
    """
    all_related = []
    for c_tbl in current_tbls:
        [all_related.append(val) for val in d_rlts[c_tbl] if val not in current_tbls]
    return list(set(all_related))


def query_format(str):
    """
    Formatting the string like we want it to be presented
    :param str:     (String) The query
    :return:        (String) Formatted Query
    """
    dct = {'FROM': '\nFROM', ' WHERE': '\nWHERE', ' AND ': '\nAND '}
    for r in (('FROM', '\nFROM'), (' WHERE', '\nWHERE'), (' AND ', '\nAND ')):
        str = str.replace(*r)
    return str


def create_txt_lbl(frm, txt, wrpln=250, hig=5, anc="w", wid=20, jst='left', lbl_pack=False):
    """
    Create labels with text inside
    :param frm:         Father frame
    :param txt:         Label's value
    :param wrpln:       wraplength
    :param hig:         height
    :param anc:         anchor
    :param wid:         width
    :param jst:         justify
    :param lbl_pack:    if needed to be packed
    :return: my_text (StringVar), lbl_text (Label)
    """
    my_txt = StringVar()
    my_txt.set(txt)
    lbl_txt = Label(frm, textvariable=my_txt, wraplength=wrpln, font=myfont,
                    height=hig, anchor=anc, width=wid, justify=jst, fg='midnightblue')
    if lbl_pack:
        lbl_txt.pack()
    return my_txt, lbl_txt


def create_text_wid(frame, str, height, width):
    """
    Creates Text Widget
    :param frame:   Text's frame
    :param str:     (String) Text inside widget
    :param height:  (int) Widget's height
    :param width:   (int) Widget's weight
    :return:        TextWidget and connected scrollbar
    """
    txt = Text(frame, height=height, width=width)
    txt.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
    txt.configure(font=myfont)
    txt.insert(tkinter.END, str)
    txt.config(state=DISABLED)
    scb = Scrollbar(frame, command=txt.yview)
    scb.grid(row=0, column=1, sticky='nsew')
    txt['yscrollcommand'] = scb.set
    return txt, scb

