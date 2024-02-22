import sqlite3
import csv
from os import path

ROOT = path.dirname(path.realpath("database.db"))

def createDatabase(conn):
    con = conn.cursor()
    con.execute('''CREATE TABLE programs(
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            grades TEXT NOT NULL,
            type TEXT NOT NULL,
            field TEXT NOT NULL,
            desc TEXT NOT NULL
    );''')


    con.execute('''CREATE TABLE comments(
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                content TEXT NOT NULL
        );''')

def deleteProgramTable(conn):
    sql = 'DROP TABLE programs;'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    
def deleteCommentTable(conn):
    sql = 'DROP TABLE comments;'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def deleteAllPrograms(conn):

    sql = 'DELETE FROM programs'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def deleteAllComments(conn):

    sql = 'DELETE FROM comments'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def deleteProgramById(conn, id):

    sql = 'DELETE FROM programs WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def deleteCommentById(conn, id, name):

    sql = 'DELETE FROM Comments WHERE id=? AND name=?'
    cur = conn.cursor()
    cur.execute(sql, (id,name,))
    conn.commit()


def updateProgramCSVTable():
    conn = sqlite3.connect("database.db")
    conn.text_factory = str ## my current (failed) attempt to resolve this
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM programs")

    with open('programTable.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'grades', 'type', 'field', 'desc'])
        writer.writerows(data)

def updateCommentCSVTable():
    conn = sqlite3.connect("database.db")
    conn.text_factory = str ## my current (failed) attempt to resolve this
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM comments")

    with open('commentTable.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'content'])
        writer.writerows(data)

def addProgram(conn, content):
    try:
        sql = ''' INSERT INTO programs(name,grades,type,field,desc)
                VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, content)
        conn.commit()
    except Exception as e:
        print(e)
        return"failure"
        

def addComment(conn, content):
    try:
        sql = ''' INSERT INTO comments(id,name,content)
                VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, content)
        conn.commit()
    except:
        return "invalid inputs"

def getProgramInfoByID(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT * FROM programs WHERE id=?", (priority,))
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramInfoByName(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT * FROM programs WHERE name=? ORDER BY name", (priority,))
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramInfoByGrade(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT * FROM programs WHERE lower(instr(grades, ?)) > 0", (priority,))
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramInfoByField(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT * FROM programs WHERE instr(field, ?) > 0", (priority,))
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramInfoBySearch(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT * FROM programs WHERE (grades LIKE ? OR ? = '') AND (type LIKE ? OR ? = '') AND (field LIKE ? OR ? = '') ORDER BY name", ('%'+priority[0]+'%', priority[0], priority[1], priority[1], '%'+priority[2]+'%', priority[2],))
    rows = cur.fetchall()
    print(priority)
    print(rows)
    if(rows == None):
        return "invalid input"
    return rows

def getProgramComments(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT * FROM comments WHERE id=?", (priority,))
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramNames(conn):

    cur = conn.cursor()
    cur.execute("SELECT name FROM programs")
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramInfo(conn):

    cur = conn.cursor()
    cur.execute("SELECT name, grades, field FROM programs")
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramData(conn):

    cur = conn.cursor()
    cur.execute("SELECT name, grades, type, field, desc FROM programs ORDER BY name")
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows



db = sqlite3.connect(path.join(ROOT, "database.db"))

#deleteProgramTable(db)
#deleteCommentTable(db)

#createDatabase(db)
#deleteProgramById(db,1)

#addProgram(db, ["a","a","a","a"])
#addProgram(db, ["PClassic", "all", "STEM,Computer Science,Math,Competition", "A team of 4 completes 8 problems in 4 hours."])
#addComment(db, [1,"Ronin", "I liked this course"])


#print(getProgramInfoByID(db, 1))
#print(getProgramInfoByName(db, "REx"))
#print(getProgramInfoByGrade(db, "11"))
#print(getProgramInfoByField(db, "Math"))
#print(getProgramComments(db, 1))

#print(getProgramNames(db))
#(updateCommentCSVTable())
#(updateProgramCSVTable())


