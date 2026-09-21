import sqlite3, json
from datetime import datetime
DB="factguard.db"

def init_db():
    con=sqlite3.connect(DB); cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS checks (id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT,result_json TEXT,created_at TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS appeals (id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT,created_at TEXT)")
    con.commit(); con.close()

def save_check(text,result):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO checks(text,result_json,created_at) VALUES(?,?,?)",
                (text,json.dumps(result,ensure_ascii=False),datetime.utcnow().isoformat()))
    con.commit(); con.close()

def list_checks():
    con=sqlite3.connect(DB)
    rows=con.execute("SELECT text,created_at FROM checks ORDER BY id DESC LIMIT 50").fetchall()
    con.close()
    return [{"text":r[0],"created_at":r[1]} for r in rows]

def save_appeal(text):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO appeals(text,created_at) VALUES(?,?)",
                (text,datetime.utcnow().isoformat()))
    con.commit(); con.close()
