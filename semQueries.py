import sqlite3


def db_connector(db):
    """
    Pointing to DB
    :param db: (string) path to DB location
    :return:  cursor pointing to DB
    """
    conn = sqlite3.connect(db)
    return conn.cursor()


def tables_names(cur):
    """
    Creates list of all tables names
    :param cur: cursor
    :return: tbls - list of tables names
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
    for rlt_tbl in tbls:
        if tbl in relations[rlt_tbl]:
            return rlt_tbl
    return None


def query_creation1(tbls, tbls_num, relations, lbl_tbls, lbl_cols):
    """
    Creates query from tables and relation
    :param tbls:        list of tables' names in DB
    :param tbls_num:    (int) number of current tables.
    :param relations:   (dict) dictionary of dictionaries of table, it fk and connected tables.
    :param lbl_tbls:    (String) Label that presents the tables to the user
    :param lbl_cols:    (String) Label that presents the FK to the user
    :return:            (String) The query
    """

    # Query's base
    tbls_set = set()
    q_where = f' WHERE '
    str_relation = ''
    for i in range(tbls_num - 1):
        if 0 < i:  # Add one more table
            q_where += ' AND '
            str_relation += '\n\n'
        rlt_tbl = find_related_tbl(tbls[i], tbls, relations)
        tbls_set.add(tbls[i])   # Add to set
        tbls_set.add(rlt_tbl)   # Add to set

        str_relation += f'Table: {tbls[i]:<16} \tTable: {rlt_tbl:<16} \tFK: {relations[tbls[i]][rlt_tbl]}'
        q_where += f'{tbls[i]}.{relations[tbls[i]][rlt_tbl]} = {rlt_tbl}.{relations[rlt_tbl][tbls[i]]}'

    if tbls_num == 1:
        q_where = ''
        str_relation = 'No Joined tables'
    lbl_tbls.set(str_relation)

    q_select = f'SELECT * FROM {tbls[0]}'
    for tbl in tbls_set:
        if tbl is not tbls[0]:
            q_select += f', {tbl}'

    return q_select + q_where


def query_creation(tbls, tbls_num, relations, lbl_tbls):
    """
    Creates query from tables and relation
    :param tbls:        list of tables' names in DB
    :param tbls_num:    (int) number of current tables.
    :param relations:   (dict) dictionary of dictionaries of table, it fk and connected tables.
    :param lbl_tbls:    (String) Label that presents the tables to the user
    :return:            (String) The query
    """

    # Query's base
    tbls_set = set()    # Set of all related tables (without duplicates)
    tbls_set.add(tbls[0])
    q_where = f' WHERE '
    str_relation = ''
    for i in range(tbls_num - 1):
        if 0 < i:  # Add one more table
            q_where += ' AND '
            str_relation += '\n\n'
        rlt_tbl = find_related_tbl(tbls[i], tbls, relations)
        tbls_set.add(tbls[i])   # Add to set
        tbls_set.add(rlt_tbl)   # Add to set
        str_relation += f'Table: {tbls[i]:<16} \tTable: {rlt_tbl:<16} \tFK: {relations[tbls[i]][rlt_tbl]}'
        q_where += f'{tbls[i]}.{relations[tbls[i]][rlt_tbl]} = {rlt_tbl}.{relations[rlt_tbl][tbls[i]]}'

    if tbls_num == 1:
        q_where = ''
        str_relation = 'No Joined tables'
    lbl_tbls.set(str_relation)

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


def sort_treeview_by_col(trv, col, rvs):
    """
    Sorting treeview by cols & reverse
    :param trv: (treeview) Treeview with DB from query
    :param col: (int) Index of col in trv
    :param rvs: (boolean) Reverse
    :return: None
    """
    lst = [(trv.set(k, col), k) for k in trv.get_children('')]
    try:
        lst.sort(key=lambda x: int(x[0]), reverse=rvs)
    except ValueError:
        lst.sort(reverse=rvs)

    for index, (val, k) in enumerate(lst):
        trv.move(k, '', index)  # Put in sorted placement

    trv.heading(col, command=lambda: sort_treeview_by_col(trv, col, not rvs))  # Reverse next time


def is_unrelated_to_others(checked_tbl, independent_tbl, current_tbls, d_rlts):
    """
    Checks if specific table can relay on other tables
    :param checked_tbl:         The table that we want to check
    :param independent_tbl:     The independent table
    :param current_tbls:        Relevant tables
    :param d_rlts:              (dict) Tables relations
    :return:    True if cant relay on other tables, else False
    """
    for c in current_tbls:
        if c is not independent_tbl and checked_tbl in d_rlts[c].keys():
            return False
    return True


def influanced_by(tbl, current_tbls, d_rlts):
    """
    Checks what tables depends on only specific table from the list
    :param tbl:             The specific table
    :param current_tbls:    (List) Presented tables
    :param d_rlts:          (dict) Relations
    :return: List of dependant tables
    """
    related = d_rlts[tbl].keys()
    depend = []
    for t in related:
        if is_unrelated_to_others(t,tbl, current_tbls, d_rlts):
            depend.append(t)
    return depend


def get_all_related(current_tbls, d_rlts):
    """
    Add all related tables to a list
    :param current_tbls:
    :param d_rlts:
    :return:
    """
    all_related = []
    for c_tbl in current_tbls:
        [all_related.append(val) for val in d_rlts[c_tbl] if val not in current_tbls]
    return list(set(all_related))

