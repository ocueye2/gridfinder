import sqlite3

class DB:
    def __init__(self):
        self.dbpath = "data/main.db"
    def __enter__(self):
        conn = sqlite3.connect(self.dbpath)
        self.conn = conn
        cur = conn.cursor()
        self.cur = cur
        return cur
    def __exit__(self, exc_type, exc, tb):
        conn = self.conn
        conn.commit()
        conn.close()


# db init
with DB() as db:

    # grids
    db.execute("""
        CREATE TABLE IF NOT EXISTS grids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            size TEXT
        )
        """)

        # items
    db.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            gridid INT,
            location TEXT
        )
        """)


class grid:
    def create(name,x,y):
        print(f"{name}:{x}:{y}")
        with DB() as db:
            db.execute("INSERT INTO grids (name, size) VALUES (?, ?)",
            (name,str({"x":x,"y":y}),))

    def search(term,count=20):
        with DB() as db:
            rows = db.execute("SELECT * FROM grids WHERE name LIKE ?",(f"%{term}%",))
            return rows[count:]
    
    def delete(id):
        with DB() as db:
            db.execute("DELETE FROM grids WHERE id = ?", (id,))

    def getdata(id):
        with DB() as db:
            db.execute("SELECT * FROM grids WHERE id = ?", (id,))
            row = db.fetchone()
        return row

class item:
    def create(name,gridid,points):
        with DB() as db:
            db.execute("INSERT INTO items (name, gridid, location ) VALUES (?, ?, ?)",
            (name,gridid,str(points),))

    def search(term,count=20):
        with DB() as db:
            db.execute("SELECT * FROM items WHERE name LIKE ?",(f"%{term}%",))
            rows = db.fetchall()
        return rows[count:]
    
    def delete(id):
        with DB() as db:
            db.execute("DELETE FROM items WHERE id = ?", (id,))
    
    def getdata(id):
        with DB() as db:
            db.execute("SELECT * FROM items WHERE id = ?", (id,))
            row = db.fetchone()
            return row