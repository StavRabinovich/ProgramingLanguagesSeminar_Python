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
    """    Creates list of all columns' names and if FK
    :param tbl_name: table's name
    :param cr: cursor
    :return: cols: columns' names
    """
    cols = []
    qry = 'PRAGMA table_info(' + tbl_name + ');'
    res = cr.execute(qry)
    # res row --> (idx, name, type, ?, ?, PK?)
    for row in res.fetchall():
        cols.append([row[5], row[1]])  # Saves name and if PK (isPK? , name)
    return cols


# print(get_cols('albums'))

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
    :return: relations: list of tuples (chosen table, related table, relation) .
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



#print(get_related_tables(['albums', 'tracks']))


class MyTable:
    def __init__(self, name):
        self.name = name
        self.pk = get_table_pk(name)
        self.relations_count = 0
        self.relations = []

    def add_relation(self, relation):
        self.relations_count += 1
        self.relations.append(relation)

    def remove_relation(self, relation):
        self.relations_count -= 1
        self.relations.remove(relation)

    def check_for_potential_relations(self, tbls):
        potential_relations = []
        for tbl in tbls:
            if tbl is not self.name:
                rlt = get_relating_col(self.name, tbl)
                if rlt is not None and (tbl, rlt) not in self.relations:
                    potential_relations.append(rlt)
        return potential_relations

    def init_relations(self, tables):
        self.relations = self.check_for_potential_relations(tables)
        self.relations_count = len(self.relations)

class Tables:
    def __init__(self):
        self.all_tables = tables_names()
        self.tables = list()
        self.relations = list()
        self.potential_tables = list()

    def add_table(self, table_name):
        if self.tables is []:
            self.tables.append(MyTable(table_name))
        else:
            new_tbl = MyTable(table_name)



