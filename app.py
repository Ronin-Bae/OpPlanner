import re
from datetime import datetime
import sqlite3
import csv
from data import *

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/add')
def add():
   return render_template('addProgram.html')

@app.route('/program<name>',methods=['POST','GET'])
def program(name):

    db = sqlite3.connect("database.db") 
    print(name)
    #name = str(name)[2:len(str(name))-3]
    print(name)
    data = list(getProgramInfoByName(db, name))[0]
    print(data)
    id = data[0]

    if request.method == 'POST':
        result = request.form
        n = request.form.get("Name")
        c = request.form.get("Comment")
        n = str(n)
        c = str(c)
        print(n + c)
        addComment(db,[id,n,c])
        print("comment added")
        
    
    comms = list(getProgramComments(db, id))
    comments = []
    for x in range(len(comms)):
       comments.append(comms[x][1:])
    data = data[1:]
    db.close() 
    return render_template('program.html', data=data, comms=comments)

@app.route('/catalog')
def catalog():
    db = sqlite3.connect("database.db")
    data = getProgramInfo(db)
    return render_template('catalog.html', data=data)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        p = request.form.get("Program")
        g = request.form.get("Grade")
        f = request.form.get("Field")
        d = request.form.get("Description")
        p = str(p)
        g = str(g)
        f = str(f)
        d = str(d)
        print(p+g+f+d)
        db = sqlite3.connect("database.db")
        addProgram(db, [p,g,f,d])
        db.close() 

    return render_template("result.html",result = result)

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

if __name__ == '__main__':
   app.run(debug = True)

