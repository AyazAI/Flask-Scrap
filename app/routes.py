from flask import render_template, request, redirect
from app import app, db
from app.models import Entry
import cx_Oracle      # We are an Oracle shop, and this changes some things
import csv
import json
from io import StringIO       # allows you to store response object in memory instead of on disk
from flask import Flask, make_response # Necessary imports, should be obvious
from flask import g
import sqlite3

jedi = "of the jedi"

@app.route('/')
@app.route('/index')
def index():
    # entries = [
    #     {
    #         'id' : 1,
    #         'title': 'test title 1',
    #         'description' : 'test desc 1',
    #         'status' : True
    #     },
    #     {
    #         'id': 2,
    #         'title': 'test title 2',
    #         'description': 'test desc 2',
    #         'status': False
    #     }
    # ]
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/write_csv/<int:id>')
def write_csv(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            print("Entry got")

    title = entry.title
    description = entry.description

    with open ('data.csv', mode = 'w') as file:
        emp_write= csv.writer(file , delimiter=',')
        emp_write.writerow([id, title, description])
        return "Written to CSV File"


@app.route('/write_json/<int:id>')
def write_json(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            print("Entry got")

    data = {}
    data = {
        'id': id,
        'Title': entry.title,
        'Description': entry.description
    }

    with open('json.txt', 'w') as outfile:
        json.dump(data, outfile)
        return "Written to JSON FILE"


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or description:
            entry = Entry(title = title, description = description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

    return "of the jedi"

@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "of the jedi"

@app.route('/update', methods=['POST'])
def update():
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')

    return "of the jedi"



@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')

    return "of the jedi"

@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect('/')

    return "of the jedi"

# @app.errorhandler(Exception)
# def error_page(e):
#     return "of the jedi"


@app.route('/dummy')
def dummy():
    return "dummy"

