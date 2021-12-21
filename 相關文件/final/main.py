
from flask import Flask, g
from flask import render_template
import random
from flask import request
app = Flask(__name__)
import csv
import sqlite3
import numpy as np
hot_pot_name = ['大呼過癮', '雞湯大叔', '富樂']
Store = [('12345678',20,4.5,'大呼過癮'), ('23456789',30,5,'雞湯大叔'), ('34567891',1,1,'富樂')]
SQLITE_DB_SCHEMA = 'schema.sql'
SQLITE_DB_PATH = 'test.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
        
    return db

@app.route('/reset')
def reset_db():
    with open(SQLITE_DB_SCHEMA, 'r') as f:
        create_db_sql = f.read()
    db = get_db()
    # Reset database
    # Note that CREATE/DROP table are *immediately* committed
    # even inside a transaction
    with db:
        db.execute("DROP TABLE IF EXISTS Store")
        db.execute("DROP TABLE IF EXISTS Hot_pot")
        db.executescript(create_db_sql)
    
     #hot_pot_name
    for i in hot_pot_name:
        with db:
            db.execute(
             'INSERT INTO  Hot_pot (Brand) VALUES (?)',
             (i,))
     #Store
    with db:
        db.executemany(
        'INSERT INTO  Store (Phonenumber, Comment_num, Avg_rating, Brand) VALUES (?, ?, ?, ?)',
        Store)
        
    return render_template('index.html')
        

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/show', methods=['POST'])
def draw():
    # Get the database connection
    db = get_db()
    p = ''
    table_name = request.form.get('table_name')
    print(table_name)
    if table_name == '品牌名稱':
        tbl = "<tr><td>品牌名稱</td></tr>"
        p+=tbl 
        with db:
            c = db.execute('SELECT * FROM Hot_pot')
        for row in c:
            a = "<tr><td>%s</td></tr>"%row[0]
            p+=a
        return '<html><head><title>品牌名稱的結果</title></head><body><table>{}</table></body></html>'.format(p)
         
    elif table_name == '火鍋店全名':
        tbl = "<tr><td>電話號碼</td><td>評論數</td><td>平均星數</td><td>品牌名稱</td></tr>"
        p+=tbl 
        with db:
            c = db.execute('SELECT * FROM Store')
        for row in c:
            p+="<tr>"
            for column in row:
                a = "<td>%s</td>"%column
                p+=a
            p+="</tr>"
        return '<html><head><title>火鍋店全名的結果</title></head><body><table>{}</table></body></html>'.format(p)
    else:
        return '<p>你一定要勾選一個</p>'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0" ,debug=True)