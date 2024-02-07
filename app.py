import re
from datetime import datetime
import sqlite3
import csv
from data import *

from flask import Flask
from flask import render_template
from flask import request

from os import path

ROOT = path.dirname(path.realpath("database.db"))

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./myproject')
        origin = repo.remotes.origin
        repo.create_head('master', 
    origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
        origin.pull()
        return '', 200
    else:
        return '', 400

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/add')
def add():
   return render_template('addProgram.html')

@app.route('/program<name>',methods=['POST','GET'])
def program(name):

    db = sqlite3.connect(path.join(ROOT, "database.db"))
    data = list(getProgramInfoByName(db, name))[0]
    id = data[0]

    if request.method == 'POST':
        n = request.form.get("Name")
        c = request.form.get("Comment")
        n = str(n)
        c = str(c)
        addComment(db,[id,n,c])

        
    
    comms = list(getProgramComments(db, id))
    comments = []
    for x in range(len(comms)):
       comments.append(comms[x][1:])
    data = data[1:]
    db.close() 
    return render_template('program.html', data=data, comms=comments)

@app.route('/catalog',methods=['POST','GET'])
def catalog():
    db = sqlite3.connect(path.join(ROOT, "database.db"))
    if request.method=='POST':
        grade=request.form.get("Grade")
        field=request.form.get("Field").upper()
        if(grade == "" and field == ""):
            data = getProgramData(db)
        else:
            total = getProgramInfoByGradeAndField(db,[grade, field])
            data = []
            for x in total:
                print(x)
                data.append(x[1:])

    else:
        data = getProgramData(db)
    print(data)
    return render_template('catalog.html', data=data)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        p = request.form.get("Program")
        g = request.form.get("Grade")
        f = request.form.get("Field")
        d = request.form.get("Description")
        p = str(p).capitalize()
        g = str(g).upper()
        f = str(f).upper()
        d = str(d)
        db = sqlite3.connect(path.join(ROOT, "database.db"))
        addProgram(db, [p,g,f,d])
        db.close() 

    return render_template("result.html",result = result)

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

if __name__ == '__main__':
   app.run(debug = True)

