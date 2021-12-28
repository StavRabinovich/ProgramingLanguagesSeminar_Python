import sqlite3

conn = sqlite3.connect('CnkDatabase/chinook.db')
cur = conn.cursor()

def tables_names(cr=cur):
    """
    Creates list of all tables names
    :param cr: cursor
    :return: tbls - tables names
    """
    tbls = []
    res = cr.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for row in res.fetchall():
        if row[0] != 'sqlite_sequence' and row[0] != 'sqlite_stat1':
            tbls.append(row[0])
    return tbls


chnk_tables = tables_names()  # Saves all chnk tables in chnk_tables


# print(chnk_tables)

def get_cols(tbl_name, cr=cur):
    """    Creates list of all columns' names and if PK
    :param tbl_name: table's name
    :param cr: cursor
    :return: cols: columns' names
    """
    cols = []
    qry = 'PRAGMA table_info(' + tbl_name + ');'
    res = cr.execute(qry)
    # res row --> (idx, name, type, NotNull, dflt_value, PK)
    for row in res.fetchall():
        print(row)
        cols.append([row[5], row[1]])  # Saves name and if PK (isPK , name)
    return cols

rs = cur.execute("SELECT * FROM sqlite_master WHERE ;")
for r in rs.fetchall():
    print(r)
    print()


print(get_cols('albums'))
print(get_cols('playlist_track'))

def get_table_pk(tbl_name):
    """ Creates list of FK of the table
    :param tbl_name: chosen table's name
    :return: tbl_fks: list of table's FK
    """
    cols = get_cols(tbl_name)
    tbl_fks = []
    for col in cols:
        if col[0] == 1:
            tbl_fks.append(col[1])
    return tbl_fks


# print(get_table_fk('albums'))

def get_relating_col(tbl1, tbl2):
    """
    Get the relation col
    :param tbl1:
    :param tbl2:
    :return: Column name OR None
    """
    pk_lst = get_table_pk(tbl1)
    cols = get_cols(tbl2)
    for col in cols:
        if col[1] in pk_lst:
            return col[1]
    pk_lst = get_table_pk(tbl2)
    cols = get_cols(tbl1)
    for col in cols:
        if col[1] in pk_lst:
            return col[1]
    return None

# print(get_relating_col('albums', 'tracks'))
# print(get_relating_col('albums', 'generes'))

def is_related(tbl1, tbl2):
    """
    Checks if two tables are related
    :param tbl1: first table
    :param tbl2: second table
    :return: True / False
    """
    pk_lst = get_table_pk(tbl1)
    cols = get_cols(tbl2)
    for col in cols:
        if col[1] in pk_lst:
            return True
    pk_lst = get_table_pk(tbl2)
    cols = get_cols(tbl1)
    for col in cols:
        if col[1] in pk_lst:
            return True
    return False

# print(is_related('albums', 'tracks'))
# print(is_related('albums', 'generes'))


def get_related_tables(chosen_tbls, tbls=chnk_tables):
    """ Creates list of potentially related tables' names
    :param chosen_tbls: chosen tables
    :param tbls: all tables' list
    :return: relations: list of tuples (chosen table, related table, fk) .
    """
    relations = []
    for tbl in tbls:
        if tbl not in chosen_tbls:
            # if True in (is_related(tbl, c_tbl) for c_tbl in chosen_tbls):
            #     related_tbls.append(tbl)
            for c_tbl in chosen_tbls:
                rlt = get_relating_col(c_tbl, tbl)
                if rlt is not None:
                    relations.append((c_tbl, tbl, rlt))
    return relations


def get_related(mytbl, tbls=chnk_tables):
    """
    List of related tables
    :param mytbl:
    :param tbls:
    :return: list of related tables' names
    """
    related = []
    for tbl in tbls:
        if tbl is not mytbl:
            if is_related(mytbl, tbl):
                related.append(tbl)
    return related


#print(get_related_tables(['albums', 'tracks']))

def dict_of_relations(tbls=chnk_tables):
    """
    :param tbls: all tables' names
    :return: all related
    """
    relations_d = dict()
    for tbl in tbls:
        relations_d.update({tbl, get_related(tbl)})
    return relations_d
