from tkinter import *
from tkinter import ttk
import sqlQueries as sqqr

def db(tree):   # Database
    mycursor = sqqr.conn.cursor()
    data(sqqr.conn, mycursor, tree)

def data(conn, mycursor, tree): # Data import
    for x in tree.get_children(): # Cleans tree
        tree.delete(x)
    mycursor.execute("SELECT *  FROM * WHERE artists.ArtistId = albums.ArtistId AND albums.AlbumId = tracks.AlbumId")
    for row in mycursor:
         tree.insert('', 'end', values=row[0:10])
    conn.close()


class AppWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x600") # Window size
        self.root.title("Header Title") # Header
        self.root.wm_attributes("-topmost", 1)
        self.frame = Frame(self.root).pack()

        # self.label1 = ttk.Label(self.frame, test="Label")
        # self.label1.pack()
        self.tree = ttk.Treeview(self.frame, columns=(1, 2, 3, 4, 5, 6, 7), \
                                 height=20, show="headings")
        # self.tree.bind("<Double-1>", self.on_double_click)

        self.tree.pack(side='top')


        self.root.mainloop() # Will run the App window




# __Main__
app = AppWindow()