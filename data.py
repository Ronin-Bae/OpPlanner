import sqlite3
import csv

def createDatabase():
    con.execute('''CREATE TABLE programs(
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT,
            grades TEXT,
            field TEXT,
            desc TEXT
    );''')


    con.execute('''CREATE TABLE comments(
                id INTEGER,
                name TEXT,
                content TEXT
        );''')

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
        writer.writerow(['id', 'name', 'grades', 'field', 'desc'])
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
        sql = ''' INSERT INTO programs(name,grades,field,desc)
                VALUES(?,?,?,?) '''
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
    cur.execute("SELECT * FROM programs WHERE name=?", (priority,))
    rows = cur.fetchall()
    if(rows == None):
        return "invalid input"
    return rows

def getProgramInfoByGrade(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT * FROM programs WHERE instr(grades, ?) > 0", (priority,))
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


db = sqlite3.connect('database.db')
con = db.cursor()

#createDatabase()
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
data = getProgramInfo(db)
for elem in data:
    print(elem)
print("hi")
(updateCommentCSVTable())
(updateProgramCSVTable())


